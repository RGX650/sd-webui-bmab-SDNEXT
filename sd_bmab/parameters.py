import os
import json
from sd_bmab import constants
from sd_bmab.util import debug_print


def parse_args(args):
	config = Parameters().load_preset(args)
	ar = Parameters().get_dict(args, config)
	return config, ar


class Parameters(object):
	def __init__(self) -> None:
		super().__init__()

		self.params = [
			('enabled', False),
			('preprocess_checkpoint', constants.checkpoint_default),
			('preprocess_vae', constants.vae_default),
			('txt2img_noise_multiplier', 1),
			('txt2img_extra_noise_multiplier', 0),
			('txt2img_filter_hresfix_before_upscale', 'None'),
			('txt2img_filter_hresfix_after_upscale', 'None'),
			('module_config.kohyahiresfix.enabled', False),
			('module_config.kohyahiresfix.stop1', 0.15),
			('module_config.kohyahiresfix.depth1', 3),
			('module_config.kohyahiresfix.stop2', 0.4),
			('module_config.kohyahiresfix.depth2', 4),
			('module_config.kohyahiresfix.scaler', 'bicubic'),
			('module_config.kohyahiresfix.downsampling', 0.5),
			('module_config.kohyahiresfix.upsampling', 2.0),
			('module_config.kohyahiresfix.smooth_scaling', True),
			('module_config.kohyahiresfix.early_upsampling', False),
			('module_config.kohyahiresfix.disable_additional_pass', True),
			('resample_enabled', False),
			('module_config.resample_opt.save_image', False),
			('module_config.resample_opt.hiresfix_enabled', False),
			('module_config.resample_opt.checkpoint', constants.checkpoint_default),
			('module_config.resample_opt.vae', constants.vae_default),
			('module_config.resample_opt.method', 'txt2img-1pass'),
			('module_config.resample_opt.filter', 'None'),
			('module_config.resample_opt.prompt', ''),
			('module_config.resample_opt.negative_prompt', ''),
			('module_config.resample_opt.sampler', constants.sampler_default),
			('module_config.resample_opt.scheduler', constants.scheduler_default),
			('module_config.resample_opt.upscaler', constants.fast_upscaler),
			('module_config.resample_opt.steps', 20),
			('module_config.resample_opt.cfg_scale', 7),
			('module_config.resample_opt.denoising_strength', 0.75),
			('module_config.resample_opt.strength', 0.5),
			('module_config.resample_opt.begin', 0.0),
			('module_config.resample_opt.end', 1.0),
			('pretraining_enabled', False),
			('module_config.pretraining_opt.hiresfix_enabled', False),
			('module_config.pretraining_opt.pretraining_model', None),
			('module_config.pretraining_opt.prompt', ''),
			('module_config.pretraining_opt.negative_prompt', ''),
			('module_config.pretraining_opt.sampler', constants.sampler_default),
			('module_config.pretraining_opt.scheduler', constants.scheduler_default),
			('module_config.pretraining_opt.steps', 20),
			('module_config.pretraining_opt.cfg_scale', 7),
			('module_config.pretraining_opt.denoising_strength', 0.75),
			('module_config.pretraining_opt.dilation', 4),
			('module_config.pretraining_opt.box_threshold', 0.35),
			('edge_flavor_enabled', False),
			('edge_low_threadhold', 50),
			('edge_high_threadhold', 200),
			('edge_strength', 0.5),
			('resize_intermediate_enabled', False),
			('module_config.resize_intermediate_opt.resize_by_person', True),
			('module_config.resize_intermediate_opt.method', 'stretching'),
			('module_config.resize_intermediate_opt.alignment', 'bottom'),
			('module_config.resize_intermediate_opt.filter', 'None'),
			('module_config.resize_intermediate_opt.scale', 0.85),
			('module_config.resize_intermediate_opt.denoising_strength', 0.75),
			('refiner_enabled', False),
			('module_config.refiner_opt.checkpoint', constants.checkpoint_default),
			('module_config.refiner_opt.keep_checkpoint', True),
			('module_config.refiner_opt.prompt', ''),
			('module_config.refiner_opt.negative_prompt', ''),
			('module_config.refiner_opt.sampler', constants.sampler_default),
			('module_config.refiner_opt.scheduler', constants.scheduler_default),
			('module_config.refiner_opt.upscaler', constants.fast_upscaler),
			('module_config.refiner_opt.steps', 20),
			('module_config.refiner_opt.cfg_scale', 7),
			('module_config.refiner_opt.denoising_strength', 0.75),
			('module_config.refiner_opt.scale', 1),
			('module_config.refiner_opt.width', 0),
			('module_config.refiner_opt.height', 0),
			('contrast', 1),
			('brightness', 1),
			('sharpeness', 1),
			('color_saturation', 1),
			('color_temperature', 0),
			('noise_alpha', 0),
			('noise_alpha_final', 0),
			('input_image', None),
			('blend_enabled', False),
			('blend_alpha', 1),
			('detect_enabled', False),
			('masking_prompt', ''),
			('person_detailing_enabled', False),
			('module_config.person_detailing_opt.best_quality', False),
			('module_config.person_detailing_opt.force_1:1', False),
			('module_config.person_detailing_opt.block_overscaled_image', True),
			('module_config.person_detailing_opt.auto_upscale', True),
			('module_config.person_detailing_opt.scale', 4),
			('module_config.person_detailing_opt.dilation', 2),
			('module_config.person_detailing_opt.area_ratio', 0.1),
			('module_config.person_detailing_opt.limit', 1),
			('module_config.person_detailing_opt.background_color', 1),
			('module_config.person_detailing_opt.background_blur', 0),
			('module_config.person_detailing.denoising_strength', 0.4),
			('module_config.person_detailing.cfg_scale', 7),
			('face_detailing_enabled', False),
			('face_detailing_before_hiresfix_enabled', False),
			('module_config.face_detailing_opt.disable_extra_networks', False),
			('module_config.face_detailing_opt.sort_by', 'Score'),
			('module_config.face_detailing_opt.limit', 1),
			('module_config.face_detailing_opt.prompt0', ''),
			('module_config.face_detailing_opt.negative_prompt0', ''),
			('module_config.face_detailing_opt.prompt1', ''),
			('module_config.face_detailing_opt.negative_prompt1', ''),
			('module_config.face_detailing_opt.prompt2', ''),
			('module_config.face_detailing_opt.negative_prompt2', ''),
			('module_config.face_detailing_opt.prompt3', ''),
			('module_config.face_detailing_opt.negative_prompt3', ''),
			('module_config.face_detailing_opt.prompt4', ''),
			('module_config.face_detailing_opt.negative_prompt4', ''),
			('module_config.face_detailing_opt.override_parameter', False),
			('module_config.face_detailing.width', 512),
			('module_config.face_detailing.height', 512),
			('module_config.face_detailing.cfg_scale', 7),
			('module_config.face_detailing.steps', 20),
			('module_config.face_detailing.mask_blur', 4),
			('module_config.face_detailing_opt.sampler', constants.sampler_default),
			('module_config.face_detailing_opt.scheduler', constants.scheduler_default),
			('module_config.face_detailing.inpaint_full_res', 'Only masked'),
			('module_config.face_detailing.inpaint_full_res_padding', 32),
			('module_config.face_detailing_opt.detection_model', constants.face_detector_default),
			('module_config.face_detailing.denoising_strength', 0.4),
			('module_config.face_detailing_opt.dilation', 4),
			('module_config.face_detailing_opt.box_threshold', 0.3),
			('module_config.face_detailing_opt.skip_large_face', False),
			('module_config.face_detailing_opt.large_face_pixels', 0.26),
			('hand_detailing_enabled', False),
			('module_config.hand_detailing_opt.block_overscaled_image', True),
			('module_config.hand_detailing_opt.best_quality', False),
			('module_config.hand_detailing_opt.detailing_method', 'subframe'),
			('module_config.hand_detailing.prompt', ''),
			('module_config.hand_detailing.negative_prompt', ''),
			('module_config.hand_detailing.denoising_strength', 0.4),
			('module_config.hand_detailing.cfg_scale', 7),
			('module_config.hand_detailing_opt.auto_upscale', True),
			('module_config.hand_detailing_opt.scale', 2),
			('module_config.hand_detailing_opt.box_threshold', 0.3),
			('module_config.hand_detailing_opt.dilation', 0.1),
			('module_config.hand_detailing.inpaint_full_res', 'Whole picture'),
			('module_config.hand_detailing.inpaint_full_res_padding', 32),
			('module_config.hand_detailing_opt.additional_parameter', ''),
			('module_config.controlnet.enabled', False),
			('module_config.controlnet.with_refiner', False),
			('module_config.controlnet.noise', False),
			('module_config.controlnet.noise_strength', 0.4),
			('module_config.controlnet.noise_begin', 0.0),
			('module_config.controlnet.noise_end', 1.0),
			('resize_by_person_enabled', False),
			('module_config.resize_by_person_opt.mode', constants.resize_mode_default),
			('module_config.resize_by_person_opt.scale', 0.85),
			('module_config.resize_by_person_opt.denoising_strength', 0.4),
			('module_config.resize_by_person_opt.dilation', 10),
			('upscale_enabled', False),
			('detailing_after_upscale', True),
			('upscaler_name', 'None'),
			('upscale_ratio', 1.5),
			('postprocess_final_filter', 'None'),
			('config_file', ''),
			('preset', 'None'),
		]

		self.ext_params = [
			('hand_detailing_before_hiresfix_enabled', False),
		]

	@staticmethod
	def get_dict_from_args(args, d):
		ar = {}
		if d is not None:
			ar = d
		for p in args:
			key = p[0]
			value = p[1]
			keys = key.split('.')
			cur = ar
			if len(keys) > 1:
				key = keys[-1]
				for k in keys[:-1]:
					if k not in cur:
						cur[k] = {}
					cur = cur[k]
			cur[key] = value
		return ar

	@staticmethod
	def get_param_from_dict(prefix, d):
		arr = []
		for key, value in d.items():
			if isinstance(value, dict):
				prefixz = prefix + key + '.'
				sub = Parameters.get_param_from_dict(prefixz, value)
				arr.extend(sub)
			else:
				arr.append((prefix + key, value))
		return arr

	def get_dict(self, args, external_config):
		if isinstance(args[0], dict):
			default_args = Parameters.get_dict_from_args(self.params, None)
			default_args.update(args[0])
			return default_args
		else:
			if len(args) != len(self.params):
				debug_print('Refresh webui first.')
				raise Exception('Refresh webui first.')

			if args[0]:
				args_list = [(self.params[idx][0], v) for idx, v in enumerate(args)]
				args_list.extend(self.ext_params)
				ar = Parameters.get_dict_from_args(args_list, None)
			else:
				self.params.extend(self.ext_params)
				ar = Parameters.get_dict_from_args(self.params, None)

			if external_config:
				cfgarg = Parameters.get_param_from_dict('', external_config)
				ar = Parameters.get_dict_from_args(cfgarg, ar)
				ar['enabled'] = True

			return ar
		return None

	def get_default(self):
		return [x[1] for x in self.params]

	def get_preset(self, prompt):
		config_file = None
		newprompt = []
		for line in prompt.split('\n'):
			if line.startswith('##'):
				config_file = line[2:]
				continue
			newprompt.append(line)
		if config_file is None:
			return prompt, {}

		cfg_dir = os.path.join(os.path.dirname(__file__), "../preset")
		json_file = os.path.join(cfg_dir, f'{config_file}.json')
		if not os.path.isfile(json_file):
			debug_print(f'Not found configuration file {config_file}.json')
			return '\n'.join(newprompt), {}
		with open(json_file) as f:
			config = json.load(f)
		debug_print('Loading config', json.dumps(config, indent=2))
		return '\n'.join(newprompt), config

	def load_preset(self, args):
		name = 'None'
		for (key, value), a in zip(self.params, args):
			if key == 'preset':
				name = a
		if name == 'None':
			return {}

		cfg_dir = os.path.join(os.path.dirname(__file__), "../preset")
		json_file = os.path.join(cfg_dir, f'{name}.json')
		if not os.path.isfile(json_file):
			debug_print(f'Not found configuration file {name}.json')
			return {}
		with open(json_file) as f:
			config = json.load(f)
		debug_print('Loading config', json.dumps(config, indent=2))
		return config

	def get_save_config_name(self, args):
		name = None
		for (key, value), a in zip(self.params, args):
			if key == 'config_file':
				name = a
		if name is None:
			return 'noname'
		return name

	def load_config(self, name):
		save_dir = os.path.join(os.path.dirname(__file__), "../saved")
		with open(os.path.join(save_dir, f'{name}.json'), 'r') as f:
			loaded_dict = json.load(f)

		detailing_opt = loaded_dict.get('module_config', {}).get('face_detailing_opt', {})
		detection_model = detailing_opt.get('detection_model', constants.face_detector_default)
		if detection_model == 'GroundingDINO(face)':
			detailing_opt['detection_model'] = constants.face_detector_default
		default_args = Parameters.get_dict_from_args(self.params, None)
		loaded_args = Parameters.get_param_from_dict('', loaded_dict)
		final_dict = Parameters.get_dict_from_args(loaded_args, default_args)
		final_args = Parameters.get_param_from_dict('', final_dict)
		sort_dict = {a[0]: a[1] for a in final_args}
		ret = [sort_dict[key] for key, value in self.params]
		return ret

	def save_config(self, args):
		name = 'noname'
		for (key, value), a in zip(self.params, args):
			if key == 'config_file':
				name = a

		save_dir = os.path.join(os.path.dirname(__file__), "../saved")
		args_list = [(self.params[idx][0], v) for idx, v in enumerate(args)]
		conf = Parameters.get_dict_from_args(args_list, None)
		with open(os.path.join(save_dir, f'{name}.json'), 'w') as f:
			json.dump(conf, f, indent=2)

	def list_config(self):
		save_dir = os.path.join(os.path.dirname(__file__), "../saved")
		if not os.path.isdir(save_dir):
			os.mkdir(save_dir)

		configs = [x for x in os.listdir(save_dir) if x.endswith('.json')]

		return [x[:-5] for x in configs]

	def list_preset(self):
		presets = ['None']
		preset_dir = os.path.join(os.path.dirname(__file__), "../preset")
		configs = [x for x in os.listdir(preset_dir) if x.endswith('.json')]
		presets.extend([x[:-5] for x in configs])
		return presets
