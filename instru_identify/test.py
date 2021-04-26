import os
import torch.backends.cudnn as cudnn
import torch.utils.data
from torch.autograd import Variable
from torchvision import transforms
from data_loader import GetLoader
from model_compat import DSN
import torchvision.utils as vutils

# 全部数据训练一次称为一个epoch
def test(epoch, name):
    cuda = False
    cudnn.benchmark = True
    batch_size = 4
    image_size = 28
    p = str(8)
    model_root = 'dataset1'+p+'dataset2'

    ################
    #   load data  #
    ################
    # 图形变换
    source_img_transform = transforms.Compose([
          transforms.Resize(image_size),
          transforms.ToTensor(),  # 归一化,进行图像的灰度处理
          transforms.Lambda(lambda x: x.repeat(3, 1, 1)),  # 单通道变为三通道
          transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
    ])

    img_transform_source = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.1307,), std=(0.3081,))#?
    ])

    img_tranform_target = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
    ])

    if name == 'dataset1':
        mode = 'source'
        image_root = r'E:\study\python\instru_identify\dataset\dataset1\dataset1_test'
        # image_root.replace("\\",'/')
        test_list = r'E:\study\python\instru_identify\dataset\dataset1\dataset1_test_labels.txt'

        dataset = GetLoader(
            data_root=image_root,
            data_list=test_list,
            transform=img_transform_source,
        )
        dataloader = torch.utils.data.DataLoader(
            dataset=dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=0
        )
        # print('success')
    elif name == 'dataset2':
        mode = 'target'
        image_root = os.path.join('dataset', 'dataset2', 'dataset2_test')
        test_list = os.path.join('dataset', 'dataset2', 'dataset2_test_labels.txt')
        dataset = GetLoader(
            data_root=image_root,
            data_list=test_list,
            transform=img_tranform_target,
        )

        dataloader = torch.utils.data.DataLoader(
            dataset=dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=0 #?
        )
    else:
        print('error dataset name')

    ###############
    # load model  #
    ###############

    my_net = DSN()
    checkpoint = torch.load(os.path.join(model_root, 'dsn_epoch_' + str(epoch) + '.pth'))
    my_net.load_state_dict(checkpoint)
    my_net.eval() #?

    if cuda:
        my_net = my_net#.cuda()

    ###################
    # transform image #
    ###################

    # 这个函数对图片做了什么操作？
    def tr_image(img):
        img_new = (img + 1)/ 2
        return img_new

    # print(dataloader)
    len_dataloader = len(dataloader)
    # print(len_dataloader)
    data_iter = iter(dataloader)  # 获取迭代器

    i = 0
    n_total = 0
    n_correct = 0

    while i < len_dataloader-1:
        #print(i)
        data_input = data_iter.next()
        img, label = data_input

        batch_size = len(label)  # batch_size为一个batch中图片的数量

        input_img = torch.FloatTensor(batch_size, 3, image_size, image_size)
        class_label = torch.LongTensor(batch_size)

        if cuda:
            img = img#.cuda()
            label = label#.cuda()
            input_img = input_img#.cuda()
            class_label = class_label#.cuda()

        input_img.resize_as_(input_img).copy_(img)
        class_label.resize_as_(class_label).copy_(label)
        inputv_img = Variable(input_img) #?
        classv_label = Variable(class_label)

        # 输入网络

        result = my_net(input_data=inputv_img, mode='source', rec_scheme='share')
        pred = result[3].data.max(1, keepdim=True)[1]

        result = my_net(input_data=inputv_img, mode=mode, rec_scheme='all')
        rec_img_all = tr_image(result[-1].data)

        result = my_net(input_data=inputv_img, mode=mode, rec_scheme='share')
        rec_img_share = tr_image(result[-1].data)

        result = my_net(input_data=inputv_img, mode=mode, rec_scheme='private')
        rec_img_private = tr_image(result[-1].data)

        if i == len_dataloader-2:
            image_save_path = os.path.join(model_root, 'images')
            if not os.path.exists(image_save_path):
                os.mkdir(image_save_path)
            vutils.save_image(rec_img_all, image_save_path + '/' + name + '_rec_image_all.png', nrow=8)
            vutils.save_image(rec_img_share, image_save_path + '/' + name + 'rec_image_share.png', nrow=8)
            vutils.save_image(rec_img_private, image_save_path + '/' + name + 'rec_image_private.png', nrow=8)

        n_correct += pred.eq(classv_label.data.view_as(pred)).cpu().sum()
        n_total += batch_size

        i += 1

    accu = n_correct * 1.0/n_total
    print('epoch: %d,accuracy of the %s dataset: %f' % (epoch, name, accu))
