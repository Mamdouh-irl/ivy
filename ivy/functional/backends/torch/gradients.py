"""
Collection of PyTorch gradient functions, wrapped to fit Ivy syntax and signature.
"""

# global
import ivy
import torch
import warnings


def variable(x):
    if not x.is_leaf:
        return x.detach().requires_grad_()
    return x.clone().requires_grad_()


def is_variable(x, exclusive: bool = False):
    return isinstance(x, torch.Tensor) and x.requires_grad


def variable_data(x):
    return x.data


# noinspection PyShadowingNames
def execute_with_gradients(func, xs, retain_grads=False):
    xs = xs.to_native()
    func_ret = func(xs)
    if isinstance(func_ret, tuple):
        y = func_ret[0]
        rest = func_ret[1:]
    else:
        y = func_ret
        rest = tuple()
    y = ivy.to_native(y)
    x_grads_flat = list(
        torch.autograd.grad(
            [y],
            [v for k, v in xs.to_iterator()],
            retain_graph=retain_grads,
            create_graph=retain_grads,
        )
    )
    grads = xs.from_flat_list(x_grads_flat)
    grads = grads.to_ivy()
    y = ivy.to_ivy(y)
    if not retain_grads:
        y = ivy.stop_gradient(y)
    return (y, grads, *rest)


def stop_gradient(x, preserve_type=True):
    if is_variable(x) and preserve_type:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if x.grad_fn:
                x = x.detach()
                x.requires_grad = True
            elif x.grad:
                x.grad.data.zero_()
        return x
    return x.detach()
