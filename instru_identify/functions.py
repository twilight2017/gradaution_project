from torch.autograd import Function
import torch.nn as nn
import torch


class ReverseLayerF(Function):

    @staticmethod
    def forward(ctx, x, p):
        ctx.p = p

        return x.view_as(x)

    @staticmethod
    def backward(ctx, grad_output):
        output = grad_output.neg() * ctx.p

        return output, None

# class ReverseLayerF(Function):

#     def __init__(self, Lambda):
#         super(ReverseLayerF, self).__init__()
#         self.Lambda = Lambda

#     def forward(self, x):
#         return x.view_as(x)

#     def backward(self, grad_output):
#         grad_input = grad_output.clone()
#         return grad_input*(-self.Lambda)

#     def set_lambda(self, Lambda):
#         self.Lambda = Lambda


class MSE(nn.Module):
    def __init__(self):
        super(MSE, self).__init__()

    def forward(self, pred, real):
        diffs = torch.add(real, -pred)
        n = torch.numel(diffs.data)
        mse = torch.sum(diffs.pow(2)) / n

        return mse


class SIMSE(nn.Module):

    def __init__(self):
        super(SIMSE, self).__init__()

    def forward(self, pred, real):
        diffs = torch.add(real, - pred)
        n = torch.numel(diffs.data)
        simse = torch.sum(diffs).pow(2) / (n ** 2)

        return simse


class DiffLoss(nn.Module):

    def __init__(self):
        super(DiffLoss, self).__init__()

    def forward(self, input1, input2):

        batch_size = input1.size(0)
        input1 = input1.view(batch_size, -1)
        input2 = input2.view(batch_size, -1)

        input1_l2_norm = torch.norm(input1, p=2, dim=1, keepdim=True).detach()
        input1_l2 = input1.div(input1_l2_norm.expand_as(input1) + 1e-6)

        input2_l2_norm = torch.norm(input2, p=2, dim=1, keepdim=True).detach()
        input2_l2 = input2.div(input2_l2_norm.expand_as(input2) + 1e-6)

        diff_loss = torch.mean((input1_l2.t().mm(input2_l2)).pow(2))

        return diff_loss

class DiffLoss_tfTrans(nn.Module):  # 输入input:私有特征和input2:共有特征

    def __init__(self):
        super(DiffLoss_tfTrans, self).__init__()

    def forward(self, private_samples, shared_samples, weight=1.0):

        batch_size = private_samples.size(0)
        private_samples = private_samples.view(batch_size, -1)
        shared_samples = shared_samples.view(batch_size, -1)

        private_mean = torch.mean(private_samples, dim=0)
        shared_mean = torch.mean(shared_samples, dim=0)

        private_diff = private_samples - private_mean
        shared_diff = shared_samples - shared_mean

        private_samples_norm = torch.nn.functional.normalize(private_diff, p=2, dim=1).detach()
        shared_samples_norm = torch.nn.functional.normalize(shared_diff, p=2, dim=1).detach()

        diff_loss = torch.mean((private_samples_norm.t().mm(shared_samples_norm)).pow(2)) * weight

        return diff_loss


