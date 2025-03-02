"""
Collection of TensorFlow network layers, wrapped to fit Ivy syntax and signature.
"""

# global
import tensorflow as tf

from tensorflow.python.types.core import Tensor


def conv1d(
    x: Tensor,
    filters: Tensor,
    strides: int,
    padding: str,
    data_format: str = "NWC",
    dilations: int = 1,
) -> Tensor:
    if data_format == "NCW":
        x = tf.transpose(x, (0, 1, 2))
    res = tf.nn.conv1d(x, filters, strides, padding, "NWC", dilations)
    if data_format == "NCW":
        res = tf.transpose(res, (0, 1, 2))
    return res


conv1d_transpose = lambda x, filters, strides, padding, output_shape=None, data_format="NWC", dilations=1: tf.nn.conv1d_transpose(
    x, filters, output_shape, strides, padding, data_format, dilations
)


def conv2d(x, filters, strides, padding, data_format="NHWC", dilations=1):
    if data_format == "NCHW":
        x = tf.transpose(x, (0, 2, 3, 1))
    res = tf.nn.conv2d(x, filters, strides, padding, "NHWC", dilations)
    if data_format == "NCHW":
        return tf.transpose(res, (0, 3, 1, 2))
    return res


conv2d_transpose = lambda x, filters, strides, padding, output_shape=None, data_format="NHWC", dilations=1: tf.nn.conv2d_transpose(
    x, filters, output_shape, strides, padding, data_format, dilations
)


def depthwise_conv2d(x, filters, strides, padding, data_format="NHWC", dilations=1):
    filters = tf.expand_dims(filters, -1)
    strides = [1, strides, strides, 1]
    dilations = [dilations, dilations]
    return tf.nn.depthwise_conv2d(x, filters, strides, padding, data_format, dilations)


# noinspection PyDefaultArgument
def conv3d(x, filters, strides, padding, data_format="NDHWC", dilations=1):
    strides = [1] * 2 + ([strides] * 3 if isinstance(strides, int) else strides)
    dilations = [1] * 2 + ([dilations] * 3 if isinstance(dilations, int) else dilations)
    return tf.nn.conv3d(x, filters, strides, padding, data_format, dilations)


conv3d_transpose = lambda x, filters, strides, padding, output_shape=None, data_format="NDHWC", dilations=1: tf.nn.conv3d_transpose(
    x, filters, output_shape, strides, padding, data_format, dilations
)
