import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy import signal

def harmonic_with_noise(x, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, noise=None):
    y = amplitude * np.sin(2 * np.pi * frequency * x + phase)
    if show_noise:
        if noise is None:
            noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(x))
        y += noise
    return y, noise

amplitude = 1.0
frequency = 1.0
phase = 0.0
noise_mean = 0.0
noise_covariance = 0.1
show_noise = True
show_filtered = False
filter_cutoff = 0.1

x = np.linspace(0, 2, 500)
current_noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(x))

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.55)
y, current_noise = harmonic_with_noise(x, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, current_noise)
l, = plt.plot(x, y, lw=2)
l_filt, = plt.plot(x, y, lw=2, color='orange', label='Filtered')
l_filt.set_visible(False)

l_harmonic, = plt.plot(x, amplitude * np.sin(2 * np.pi * frequency * x + phase), lw=2, color='red', linestyle='--')
l_harmonic.set_visible(False)

ax.grid()

axamp = plt.axes([0.25, 0.45, 0.65, 0.03])
axfreq = plt.axes([0.25, 0.40, 0.65, 0.03])
axphase = plt.axes([0.25, 0.35, 0.65, 0.03])
axmean = plt.axes([0.25, 0.30, 0.65, 0.03])
axcov = plt.axes([0.25, 0.25, 0.65, 0.03])
axcutoff = plt.axes([0.25, 0.20, 0.65, 0.03])

samp = Slider(axamp, 'Amplitude', 0.1, 5.0, valinit=amplitude)
sfreq = Slider(axfreq, 'Frequency', 0.1, 5.0, valinit=frequency)
sphase = Slider(axphase, 'Phase', 0.0, 2 * np.pi, valinit=phase)
smean = Slider(axmean, 'Noise Mean', -1.0, 1.0, valinit=noise_mean)
scov = Slider(axcov, 'Noise Covariance', 0.0, 1.0, valinit=noise_covariance)
scutoff = Slider(axcutoff, 'Filter Cutoff', 0.05, 0.5, valinit=filter_cutoff)

rax = plt.axes([0.025, 0.7, 0.15, 0.15])
check = CheckButtons(rax, ['Show Noise'], [show_noise])

rax_filt = plt.axes([0.025, 0.55, 0.15, 0.15])
check_filt = CheckButtons(rax_filt, ['Show Filtered'], [show_filtered])

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color='lightgray')

def update(val):
    global current_noise
    amp = samp.val
    freq = sfreq.val
    ph = sphase.val
    mean = smean.val
    cov = scov.val
    cutoff = scutoff.val
    noise_visible = check.get_status()[0]
    filt_visible = check_filt.get_status()[0]

    if mean != smean.val or cov != scov.val:
        current_noise = np.random.normal(mean, np.sqrt(cov), len(x))

    y, _ = harmonic_with_noise(x, amp, freq, ph, mean, cov, noise_visible, current_noise)
    l.set_ydata(y)

    harmonic_background = amp * np.sin(2 * np.pi * freq * x + ph)
    l_harmonic.set_ydata(harmonic_background)

    if noise_visible:
        l_harmonic.set_visible(True)
    else:
        l_harmonic.set_visible(False)
   
    if filt_visible:
        b, a = signal.iirfilter(8, cutoff, btype='low')
        y_filt = signal.filtfilt(b, a, y)
        l_filt.set_ydata(y_filt)
        l_filt.set_visible(True)
    else:
        l_filt.set_visible(False)

    fig.canvas.draw_idle()

def reset(event):
    global current_noise
    samp.reset()
    sfreq.reset()
    sphase.reset()
    smean.reset()
    scov.reset()
    scutoff.reset()
    check.set_active(0)
    check_filt.set_active(0)
    current_noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(x))
    update(None)

samp.on_changed(update)
sfreq.on_changed(update)
sphase.on_changed(update)
smean.on_changed(update)
scov.on_changed(update)
scutoff.on_changed(update)
check.on_clicked(update)
check_filt.on_clicked(update)
button.on_clicked(reset)

plt.show()
