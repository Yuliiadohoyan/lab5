import numpy as np  
from bokeh.plotting import figure, curdoc  
from bokeh.models import ColumnDataSource, Slider, Button, CheckboxGroup, Select  
from bokeh.layouts import column, row 

def custom_filter(signal, window_size=5):
    filtered = np.convolve(signal, np.ones(window_size)/window_size, mode='same')
    return filtered

def harmonic_with_noise(x, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, noise=None):
    y_clean = amplitude * np.sin(2 * np.pi * frequency * x + phase)
    noise = noise if noise is not None else np.zeros_like(x)
    y_noisy = y_clean + noise if show_noise else y_clean
    return y_clean, noise, y_noisy

x = np.linspace(0, 2, 500)
amplitude = 1.0
frequency = 1.0
phase = 0.0
noise_mean = 0.0
noise_covariance = 0.1
show_noise = True

current_noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(x))

y_clean, current_noise, y_noisy = harmonic_with_noise(x, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, current_noise)
source_clean = ColumnDataSource(data=dict(x=x, y=y_clean))
source_noise = ColumnDataSource(data=dict(x=x, y=y_noisy))
source_filtered = ColumnDataSource(data=dict(x=x, y=custom_filter(y_noisy)))
p_clean = figure(title="Harmonic ", width=700, height=200)
p_clean.line('x', 'y', source=source_clean, line_width=2, color="green")
p_noise = figure(title="Noisy Harmonic Signal", width=700, height=200)
line_noise = p_noise.line('x', 'y', source=source_noise, line_width=2, color="blue")

p_filtered = figure(title="Filtered Signal", width=700, height=200)
p_filtered.line('x', 'y', source=source_filtered, line_width=2, color="orange")

amp_slider = Slider(start=0.1, end=5, value=amplitude, step=0.1, title="Amplitude")
freq_slider = Slider(start=0.1, end=5, value=frequency, step=0.1, title="Frequency")
phase_slider = Slider(start=0, end=2*np.pi, value=phase, step=0.1, title="Phase")
mean_slider = Slider(start=-1.0, end=1.0, value=noise_mean, step=0.05, title="Noise Mean")
cov_slider = Slider(start=0.0, end=1.0, value=noise_covariance, step=0.05, title="Noise Variance")
noise_checkbox = CheckboxGroup(labels=["Show Noise"], active=[0])
style_select = Select(title="Line Style", value="solid", options=["solid", "dashed", "dotted"])
reset_button = Button(label="Reset", button_type="success")
noise_params = {'mean': noise_mean, 'cov': noise_covariance}

def update(attr, old, new):
    global current_noise, noise_params

    amp = amp_slider.value
    freq = freq_slider.value
    phase = phase_slider.value
    mean = mean_slider.value
    cov = cov_slider.value
    show_noise = 0 in noise_checkbox.active

    if mean != noise_params['mean'] or cov != noise_params['cov']:
        current_noise = np.random.normal(mean, np.sqrt(cov), len(x))
        noise_params['mean'] = mean
        noise_params['cov'] = cov

    y_clean, _, y_noisy = harmonic_with_noise(x, amp, freq, phase, mean, cov, show_noise, current_noise)

    source_clean.data = dict(x=x, y=y_clean)
    source_noise.data = dict(x=x, y=y_noisy)
    source_filtered.data = dict(x=x, y=custom_filter(y_noisy))

    line_noise.glyph.line_dash = style_select.value

for widget in [amp_slider, freq_slider, phase_slider, mean_slider, cov_slider, noise_checkbox, style_select]:
    widget.on_change('value' if not isinstance(widget, CheckboxGroup) else 'active', update)

def reset():
    amp_slider.value = amplitude
    freq_slider.value = frequency
    phase_slider.value = phase
    mean_slider.value = noise_mean
    cov_slider.value = noise_covariance
    noise_checkbox.active = [0]
    style_select.value = "solid"

reset_button.on_click(reset)

layout = column(
    p_clean,
    p_noise,
    p_filtered,
    row(column(amp_slider, freq_slider, phase_slider), column(mean_slider, cov_slider)),
    row(noise_checkbox, style_select, reset_button)
)

curdoc().add_root(layout)