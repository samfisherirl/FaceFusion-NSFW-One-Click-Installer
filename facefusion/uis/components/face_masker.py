from typing import List, Optional, Tuple

import gradio

import facefusion.choices
from facefusion import state_manager, wording
from facefusion.common_helper import calc_float_step, calc_int_step
from facefusion.typing import FaceMaskRegion, FaceMaskType
from facefusion.uis.core import register_ui_component

FACE_MASK_TYPES_CHECKBOX_GROUP : Optional[gradio.CheckboxGroup] = None
FACE_MASK_REGIONS_CHECKBOX_GROUP : Optional[gradio.CheckboxGroup] = None
FACE_MASK_BLUR_SLIDER : Optional[gradio.Slider] = None
FACE_MASK_PADDING_TOP_SLIDER : Optional[gradio.Slider] = None
FACE_MASK_PADDING_RIGHT_SLIDER : Optional[gradio.Slider] = None
FACE_MASK_PADDING_BOTTOM_SLIDER : Optional[gradio.Slider] = None
FACE_MASK_PADDING_LEFT_SLIDER : Optional[gradio.Slider] = None


def render() -> None:
	global FACE_MASK_TYPES_CHECKBOX_GROUP
	global FACE_MASK_REGIONS_CHECKBOX_GROUP
	global FACE_MASK_BLUR_SLIDER
	global FACE_MASK_PADDING_TOP_SLIDER
	global FACE_MASK_PADDING_RIGHT_SLIDER
	global FACE_MASK_PADDING_BOTTOM_SLIDER
	global FACE_MASK_PADDING_LEFT_SLIDER

	has_box_mask = 'box' in state_manager.get_item('face_mask_types')
	has_region_mask = 'region' in state_manager.get_item('face_mask_types')
	FACE_MASK_TYPES_CHECKBOX_GROUP = gradio.CheckboxGroup(
		label = wording.get('uis.face_mask_types_checkbox_group'),
		choices = facefusion.choices.face_mask_types,
		value = state_manager.get_item('face_mask_types')
	)
	FACE_MASK_REGIONS_CHECKBOX_GROUP = gradio.CheckboxGroup(
		label = wording.get('uis.face_mask_regions_checkbox_group'),
		choices = facefusion.choices.face_mask_regions,
		value = state_manager.get_item('face_mask_regions'),
		visible = has_region_mask
	)
	FACE_MASK_BLUR_SLIDER = gradio.Slider(
		label = wording.get('uis.face_mask_blur_slider'),
		step = calc_float_step(facefusion.choices.face_mask_blur_range),
		minimum = facefusion.choices.face_mask_blur_range[0],
		maximum = facefusion.choices.face_mask_blur_range[-1],
		value = state_manager.get_item('face_mask_blur'),
		visible = has_box_mask
	)
	with gradio.Group():
		with gradio.Row():
			FACE_MASK_PADDING_TOP_SLIDER = gradio.Slider(
				label = wording.get('uis.face_mask_padding_top_slider'),
				step = calc_int_step(facefusion.choices.face_mask_padding_range),
				minimum = facefusion.choices.face_mask_padding_range[0],
				maximum = facefusion.choices.face_mask_padding_range[-1],
				value = state_manager.get_item('face_mask_padding')[0],
				visible = has_box_mask
			)
			FACE_MASK_PADDING_RIGHT_SLIDER = gradio.Slider(
				label = wording.get('uis.face_mask_padding_right_slider'),
				step = calc_int_step(facefusion.choices.face_mask_padding_range),
				minimum = facefusion.choices.face_mask_padding_range[0],
				maximum = facefusion.choices.face_mask_padding_range[-1],
				value = state_manager.get_item('face_mask_padding')[1],
				visible = has_box_mask
			)
		with gradio.Row():
			FACE_MASK_PADDING_BOTTOM_SLIDER = gradio.Slider(
				label = wording.get('uis.face_mask_padding_bottom_slider'),
				step = calc_int_step(facefusion.choices.face_mask_padding_range),
				minimum = facefusion.choices.face_mask_padding_range[0],
				maximum = facefusion.choices.face_mask_padding_range[-1],
				value = state_manager.get_item('face_mask_padding')[2],
				visible = has_box_mask
			)
			FACE_MASK_PADDING_LEFT_SLIDER = gradio.Slider(
				label = wording.get('uis.face_mask_padding_left_slider'),
				step = calc_int_step(facefusion.choices.face_mask_padding_range),
				minimum = facefusion.choices.face_mask_padding_range[0],
				maximum = facefusion.choices.face_mask_padding_range[-1],
				value = state_manager.get_item('face_mask_padding')[3],
				visible = has_box_mask
			)
	register_ui_component('face_mask_types_checkbox_group', FACE_MASK_TYPES_CHECKBOX_GROUP)
	register_ui_component('face_mask_regions_checkbox_group', FACE_MASK_REGIONS_CHECKBOX_GROUP)
	register_ui_component('face_mask_blur_slider', FACE_MASK_BLUR_SLIDER)
	register_ui_component('face_mask_padding_top_slider', FACE_MASK_PADDING_TOP_SLIDER)
	register_ui_component('face_mask_padding_right_slider', FACE_MASK_PADDING_RIGHT_SLIDER)
	register_ui_component('face_mask_padding_bottom_slider', FACE_MASK_PADDING_BOTTOM_SLIDER)
	register_ui_component('face_mask_padding_left_slider', FACE_MASK_PADDING_LEFT_SLIDER)


def listen() -> None:
	FACE_MASK_TYPES_CHECKBOX_GROUP.change(update_face_mask_types, inputs = FACE_MASK_TYPES_CHECKBOX_GROUP, outputs = [ FACE_MASK_TYPES_CHECKBOX_GROUP, FACE_MASK_REGIONS_CHECKBOX_GROUP, FACE_MASK_BLUR_SLIDER, FACE_MASK_PADDING_TOP_SLIDER, FACE_MASK_PADDING_RIGHT_SLIDER, FACE_MASK_PADDING_BOTTOM_SLIDER, FACE_MASK_PADDING_LEFT_SLIDER ])
	FACE_MASK_REGIONS_CHECKBOX_GROUP.change(update_face_mask_regions, inputs = FACE_MASK_REGIONS_CHECKBOX_GROUP, outputs = FACE_MASK_REGIONS_CHECKBOX_GROUP)
	FACE_MASK_BLUR_SLIDER.release(update_face_mask_blur, inputs = FACE_MASK_BLUR_SLIDER)
	face_mask_padding_sliders = [ FACE_MASK_PADDING_TOP_SLIDER, FACE_MASK_PADDING_RIGHT_SLIDER, FACE_MASK_PADDING_BOTTOM_SLIDER, FACE_MASK_PADDING_LEFT_SLIDER ]
	for face_mask_padding_slider in face_mask_padding_sliders:
		face_mask_padding_slider.release(update_face_mask_padding, inputs = face_mask_padding_sliders)


def update_face_mask_types(face_mask_types : List[FaceMaskType]) -> Tuple[gradio.CheckboxGroup, gradio.CheckboxGroup, gradio.Slider, gradio.Slider, gradio.Slider, gradio.Slider, gradio.Slider]:
	face_mask_types = face_mask_types or facefusion.choices.face_mask_types
	state_manager.set_item('face_mask_types', face_mask_types)
	has_box_mask = 'box' in face_mask_types
	has_region_mask = 'region' in face_mask_types
	return gradio.CheckboxGroup(value = state_manager.get_item('face_mask_types')), gradio.CheckboxGroup(visible = has_region_mask), gradio.Slider(visible = has_box_mask), gradio.Slider(visible = has_box_mask), gradio.Slider(visible = has_box_mask), gradio.Slider(visible = has_box_mask), gradio.Slider(visible = has_box_mask)


def update_face_mask_regions(face_mask_regions : List[FaceMaskRegion]) -> gradio.CheckboxGroup:
	face_mask_regions = face_mask_regions or facefusion.choices.face_mask_regions
	state_manager.set_item('face_mask_regions', face_mask_regions)
	return gradio.CheckboxGroup(value = state_manager.get_item('face_mask_regions'))


def update_face_mask_blur(face_mask_blur : float) -> None:
	state_manager.set_item('face_mask_blur', face_mask_blur)


def update_face_mask_padding(face_mask_padding_top : float, face_mask_padding_right : float, face_mask_padding_bottom : float, face_mask_padding_left : float) -> None:
	face_mask_padding = (int(face_mask_padding_top), int(face_mask_padding_right), int(face_mask_padding_bottom), int(face_mask_padding_left))
	state_manager.set_item('face_mask_padding', face_mask_padding)
