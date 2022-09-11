import torch


def normalize_latent(x, max_val=1.7, quantile_val=0.975):
    x = x.detach().clone()
    for i in range(x.shape[0]):
        for chl in range(4):
            channel_std = x[i, chl, :, :].std()
            if channel_std > 1.0:
                x[i, chl, :, :] = x[i, chl, :, :] / channel_std
            s = torch.quantile(torch.abs(x[i, chl, :, :]), quantile_val)
            s = torch.maximum(s, torch.ones_like(s) * max_val)
            x[i, chl, :, :] = x[i, chl, :, :] / (s / max_val)
    return x