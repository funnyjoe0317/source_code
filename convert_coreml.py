import tensorflow as tf
import coremltools as ct
import solvers.NAFNet.plane_arch

tf_model = tf.keras.models.load_model('deblur_plainet_v2')
coreml_model = ct.convert(tf_model, convert_to='mlprogram', inputs=[ct.ImageType(shape=(1, 1080, 1920, 3))], minimum_deployment_target=ct.target.iOS15, compute_precision=ct.precision.FLOAT16)
coreml_model.save('deblur_plainet_v2.mlpackage')