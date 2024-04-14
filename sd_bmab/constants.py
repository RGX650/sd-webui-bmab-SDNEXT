sampler_default = 'Use same sampler'
scheduler_default = 'Use same scheduler'
resize_mode_default = 'Intermediate'
checkpoint_default = 'Use same checkpoint'
vae_default = 'Use same vae'
fast_upscaler = 'BMAB fast'
filter_default = 'None'
face_detector_default = 'BMAB Face(Normal)'

checkpoint_description = '''
<span style="color: gray">
Specify Checkpoint and VAE to be used in BMAB.<br>
It applies to all functions, and if you change it to Checkpoint and VAE that exist for each function,<br>
it will be applied to all subsequent processes.</span>
'''


resize_description = '''

<span style="color: gray">
<br>
txt2img --<span style="color: green">resize</span>--> hires.fix --> BMAB Preprocess --> BMAB<br>
txt2img --<span style="color: green">resize</span>--> BMAB Preprocess --> BMAB<br>
<br>
Methods<br>   
stretching : Fast process. Please denoising strength should be over <span style="color: red">0.6</span>. (Only CPU).<br>
inpaint : Slow process but High quality. Repaint stretching image. (Use GPU).<br>
inpaint+lama : Very slow process but Very high quality. Repaint stretching image using ControlNet inpaint_only+lama (Use GPU with FIRE!!).<br>
inpaint_only : Very slow process but Very high quality. Repaint stretching image using ControlNet inpaint_only (Use GPU with FIRE!!).<br>
<br>
<span style="color: red">Please DO NOT SET Latent upscaler in hires.fix.</span>
</span>
'''

kohya_hiresfix_description = '''
<span style="color: gray">
This is EXPERIMENTAL function.
</span>
'''
