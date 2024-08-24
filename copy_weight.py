import tensorflow as tf
import tensorflow_model_optimization as tfmot
from solvers.NAFNet.plane_arch import PlaneNet_original, LossLayer
from solvers.networks.devblock import WsConv2D
from solvers.networks.repblock import RepBlock
from solvers.solver import DefaultOutputQuantizeConfig, NoOpQuantizeConfig, Conv2DxQuantizeConfig, DepthwiseConv2DQuantizeConfig, DefaultBNQuantizeConfig, RepBlockQuantizeConfig

import cv2
import numpy as np

def cfg_quantization(layer):
    print(layer.name)
    if 'clip_func' in layer.name:
        print('--> clip_func done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
    if 'pad_func' in layer.name:
        print('--> pad_func done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
    if 'LossLayer' in layer.name:
        print('--> LossLayer done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=NoOpQuantizeConfig())
    if 'depth_to_space' in layer.name:
        print('--> depth_to_space done')
        #return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=NoOpQuantizeConfig())
    if 'lambda' in layer.name:
        print('--> lambda done, but you should check quantization config!!')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=NoOpQuantizeConfig())
    if 'rescaling' in layer.name:
        print('--> rescaling done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=NoOpQuantizeConfig())
    if 'ws_conv2d' in layer.name:
        print('--> ws done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=Conv2DxQuantizeConfig())
    if isinstance(layer, tf.keras.layers.Conv2D):
        print('--> cv done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=Conv2DxQuantizeConfig())
    if isinstance(layer, tf.keras.layers.DepthwiseConv2D):
        print('--> dw-cv done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DepthwiseConv2DQuantizeConfig())
    if isinstance(layer, tf.keras.layers.BatchNormalization):
        print('--> BN done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultBNQuantizeConfig())
    if 'concatenate' in layer.name:
        print('--> cc done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
    if 'rep_block' in layer.name:
        print('--> rb done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=RepBlockQuantizeConfig())
    if 'multiply' in layer.name:
        print('--> multiply done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
    if 'add' in layer.name:
        print('--> add done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
    if 'global_average_pooling2' in layer.name:
        print('--> global_average_pooling2 done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
    if 'up_sampling2d' in layer.name:
        print('--> UpSampling2D done, but you should check quantization config!!')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=NoOpQuantizeConfig())
    if 'split' in layer.name:
        print('--> split!!')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=NoOpQuantizeConfig())
    if isinstance(layer, tf.keras.layers.LayerNormalization):
    #if 'layer_normalization_1' in layer.name:
        print('--> LN done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=NoOpQuantizeConfig())
        # return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())


    return layer

def load_qat_model(model):    
    annotate_model = tf.keras.models.clone_model(model, clone_function=cfg_quantization)
    annotate_model = tfmot.quantization.keras.quantize_annotate_model(annotate_model)
    
    with tfmot.quantization.keras.quantize_scope(
        {'NoOpQuantizeConfig': NoOpQuantizeConfig, 
         'Conv2DxQuantizeConfig': Conv2DxQuantizeConfig,
         'DepthwiseConv2DQuantizeConfig': DepthwiseConv2DQuantizeConfig,
         'WsConv2D': WsConv2D,
         'DefaultBNQuantizeConfig': DefaultBNQuantizeConfig,
         'DefaultOutputQuantizeConfig': DefaultOutputQuantizeConfig,
         'RepBlock': RepBlock,
         'RepBlockQuantizeConfig': RepBlockQuantizeConfig,
         'LossLayer': LossLayer,
         'tf': tf}):
        
        model = tfmot.quantization.keras.quantize_apply(annotate_model)
    
    return model

model = tf.keras.models.load_model('PlaneNet_bs16ps256_lr1e-3_e100_reg0_ch16_1219_micro07')
"""
with tfmot.quantization.keras.quantize_scope(
        {'NoOpQuantizeConfig': NoOpQuantizeConfig, 
         'Conv2DxQuantizeConfig': Conv2DxQuantizeConfig,
         'DepthwiseConv2DQuantizeConfig': DepthwiseConv2DQuantizeConfig,
         'WsConv2D': WsConv2D,
         'DefaultBNQuantizeConfig': DefaultBNQuantizeConfig,
         'DefaultOutputQuantizeConfig': DefaultOutputQuantizeConfig,
         'RepBlock': RepBlock,
         'RepBlockQuantizeConfig': RepBlockQuantizeConfig,
         'LossLayer': LossLayer,
         'tf': tf}):
    model = tf.keras.models.load_model('deblur_plainet_v2_QAT')
model.summary()
"""

#new_model = PlaneNet_original_pad(channels=16)
new_model = PlaneNet_original(channels=16)
#new_model = load_qat_model(new_model)
#new_model.set_weights(model.get_weights())
new_model.trainable = False
new_model.summary()

"""
new_model.layers[0].set_weights(model.layers[0].get_weights())
new_model.layers[1].set_weights(model.layers[1].get_weights())
new_model.layers[2].set_weights(model.layers[-1].get_weights())
for i in range(2, len(model.layers)):
    new_model.layers[i+1].set_weights(model.layers[i].get_weights())
new_model.layers[-1].set_weights(model.layers[-1].get_weights())
"""

#new_model.set_weights(model.get_weights())

new_model.save('deblur_plainet_v3_dummy_v2', overwrite=True, include_optimizer=True, save_format='tf')

"""
img = cv2.imread('003.png')
h, w, _ = img.shape
img = np.expand_dims(img, axis=0)
pad_img = np.pad(img, ((0, 0), (0, 2160 - h), (0, 3840 - w), (0, 0)))
out = new_model(pad_img).numpy().squeeze(axis=0)
cv2.imwrite('003_out.png', out[0:h, 0:w, :])
"""