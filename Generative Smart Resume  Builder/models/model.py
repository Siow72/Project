import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class VAE(nn.Module):
    def __init__(self, input_dim, hidden_dim=256, latent_dim=64):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(input_dim, hidden_dim), nn.ReLU())
        self.mu = nn.Linear(hidden_dim, latent_dim)
        self.logvar = nn.Linear(hidden_dim, latent_dim)
        self.dec = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim), nn.ReLU(),
            nn.Linear(hidden_dim, input_dim),
        )

    def encode(self, x):
        h = self.enc(x)
        return self.mu(h), self.logvar(h)

    def reparameterize(self, mu, logvar):
        if not self.training:
            return mu
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        return self.dec(z)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        x_hat = self.decode(z)
        return x_hat, mu, logvar, z
        
class TwoTowerVAE(nn.Module):
    def __init__(self, input_dim_c, input_dim_j, hidden_dim=256, latent_dim=64):
        super().__init__()
        if input_dim_c == input_dim_j:
            shared = VAE(input_dim_c, hidden_dim, latent_dim)
            self.c_tower = shared
            self.j_tower = shared

    def forward(self, xc, xj):
        xc_hat, mu_c, logvar_c, zc = self.c_tower(xc)
        xj_hat, mu_j, logvar_j, zj = self.j_tower(xj)

        emb_c = F.normalize(mu_c, dim=1)
        emb_j = F.normalize(mu_j, dim=1)

        # cosine similarity as prediction in [-1, 1], shape (B,1)
        y_hat = (emb_c * emb_j).sum(dim=1, keepdim=True)

        return xc_hat, xj_hat, mu_c, logvar_c, mu_j, logvar_j, y_hat