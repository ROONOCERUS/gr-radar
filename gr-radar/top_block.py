#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Tue Aug 15 15:02:49 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from baz import facsink
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import constsink_gl
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import ConfigParser
import SimpleXMLRPCServer
import baz
import math
import threading
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/local/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.decim = decim = 64
        self._config_xlate_offset_config = ConfigParser.ConfigParser()
        self._config_xlate_offset_config.read(".grc_udp_fac")
        try: config_xlate_offset = self._config_xlate_offset_config.getfloat("main", "xlate_offset")
        except: config_xlate_offset = 0
        self.config_xlate_offset = config_xlate_offset
        self.adc_rate = adc_rate = 64000000
        self.xlate_offset_fine = xlate_offset_fine = 0
        self.xlate_offset = xlate_offset = config_xlate_offset
        self.xlate_decim = xlate_decim = 4
        self.xlate_bandwidth = xlate_bandwidth = 250000
        self.samp_rate = samp_rate = adc_rate/decim
        self._config_xlate_bandwidth_config = ConfigParser.ConfigParser()
        self._config_xlate_bandwidth_config.read(".grc_udp_fac")
        try: config_xlate_bandwidth = self._config_xlate_bandwidth_config.getfloat("main", "xlate_bandwidth")
        except: config_xlate_bandwidth = 250000
        self.config_xlate_bandwidth = config_xlate_bandwidth
        self.baseband_rate = baseband_rate = 250000

        ##################################################
        # Blocks
        ##################################################
        self.main_notebook = self.main_notebook = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.main_notebook.AddPage(grc_wxgui.Panel(self.main_notebook), "BB")
        self.main_notebook.AddPage(grc_wxgui.Panel(self.main_notebook), "Demod")
        self.main_notebook.AddPage(grc_wxgui.Panel(self.main_notebook), "Xtra")
        self.main_notebook.AddPage(grc_wxgui.Panel(self.main_notebook), "FAC")
        self.main_notebook.AddPage(grc_wxgui.Panel(self.main_notebook), "Waterfall")
        self.main_notebook.AddPage(grc_wxgui.Panel(self.main_notebook), "Quad")
        self.Add(self.main_notebook)
        _xlate_offset_fine_sizer = wx.BoxSizer(wx.VERTICAL)
        self._xlate_offset_fine_text_box = forms.text_box(
        	parent=self.main_notebook.GetPage(0).GetWin(),
        	sizer=_xlate_offset_fine_sizer,
        	value=self.xlate_offset_fine,
        	callback=self.set_xlate_offset_fine,
        	label="Fine Offset",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._xlate_offset_fine_slider = forms.slider(
        	parent=self.main_notebook.GetPage(0).GetWin(),
        	sizer=_xlate_offset_fine_sizer,
        	value=self.xlate_offset_fine,
        	callback=self.set_xlate_offset_fine,
        	minimum=-10000,
        	maximum=10000,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.main_notebook.GetPage(0).Add(_xlate_offset_fine_sizer)
        self._xlate_offset_text_box = forms.text_box(
        	parent=self.main_notebook.GetPage(0).GetWin(),
        	value=self.xlate_offset,
        	callback=self.set_xlate_offset,
        	label="Xlate Offset",
        	converter=forms.float_converter(),
        )
        self.main_notebook.GetPage(0).Add(self._xlate_offset_text_box)
        _xlate_bandwidth_sizer = wx.BoxSizer(wx.VERTICAL)
        self._xlate_bandwidth_text_box = forms.text_box(
        	parent=self.main_notebook.GetPage(0).GetWin(),
        	sizer=_xlate_bandwidth_sizer,
        	value=self.xlate_bandwidth,
        	callback=self.set_xlate_bandwidth,
        	label="Xlate BW",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._xlate_bandwidth_slider = forms.slider(
        	parent=self.main_notebook.GetPage(0).GetWin(),
        	sizer=_xlate_bandwidth_sizer,
        	value=self.xlate_bandwidth,
        	callback=self.set_xlate_bandwidth,
        	minimum=12500,
        	maximum=500000,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.main_notebook.GetPage(0).Add(_xlate_bandwidth_sizer)
        self.xmlrpc_server_0 = SimpleXMLRPCServer.SimpleXMLRPCServer(("0.0.0.0", 8080), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.main_notebook.GetPage(4).GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=50,
        	ref_scale=2.0,
        	sample_rate=250000,
        	fft_size=512,
        	fft_rate=25,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        )
        self.main_notebook.GetPage(4).Add(self.wxgui_waterfallsink2_0.win)
        self.wxgui_scopesink2_0_1 = scopesink2.scope_sink_f(
        	self.main_notebook.GetPage(5).GetWin(),
        	title="Scope Plot",
        	sample_rate=250000,
        	v_scale=10,
        	v_offset=0,
        	t_scale=.001,
        	ac_couple=True,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.main_notebook.GetPage(5).Add(self.wxgui_scopesink2_0_1.win)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_c(
        	self.main_notebook.GetPage(1).GetWin(),
        	title="Scope Plot",
        	sample_rate=250000,
        	v_scale=10,
        	v_offset=0,
        	t_scale=.001,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.main_notebook.GetPage(1).Add(self.wxgui_scopesink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.main_notebook.GetPage(0).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=50,
        	ref_scale=2.0,
        	sample_rate=250000,
        	fft_size=1024,
        	fft_rate=30,
        	average=True,
        	avg_alpha=.25,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.main_notebook.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        self.wxgui_constellationsink2_0 = constsink_gl.const_sink_c(
        	self.main_notebook.GetPage(2).GetWin(),
        	title="Constellation Plot",
        	sample_rate=54000,
        	frame_rate=15,
        	const_size=2048,
        	M=4,
        	theta=.785398,
        	loop_bw=5/100.0,
        	fmax=0.06,
        	mu=0.5,
        	gain_mu=0.005,
        	symbol_rate=18000,
        	omega_limit=0.005,
        )
        self.main_notebook.GetPage(2).Add(self.wxgui_constellationsink2_0.win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=54000,
                decimation=250000,
                taps=None,
                fractional_bw=None,
        )
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(xlate_decim, (firdes.low_pass(1, samp_rate, xlate_bandwidth/2, 1000)), xlate_offset+xlate_offset_fine, samp_rate)
        self.facsink_0 = facsink.fac_sink_c(
        	self.main_notebook.GetPage(3).GetWin(),
        	title="Fast AutoCorrelation",
        	sample_rate=samp_rate,
        	baseband_freq=0,
                y_per_div=10,
        	ref_level=50,
        	fac_size=131072,
                fac_rate=facsink.default_fac_rate,
                average=True,
        	avg_alpha=0,
        	peak_hold=False,
        )
        self.main_notebook.GetPage(3).Add(self.facsink_0.win)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_short*1, 2)
        self.blocks_interleaved_short_to_complex_0 = blocks.interleaved_short_to_complex(False, False)
        self.baz_udp_source_0 = baz.udp_source(gr.sizeof_short*2, "0.0.0.0", 28888, 16384, True, True, True, True)
        self._baseband_rate_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.baseband_rate,
        	callback=self.set_baseband_rate,
        	label="BB Rate",
        	converter=forms.float_converter(),
        )
        self.Add(self._baseband_rate_static_text)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.wxgui_scopesink2_0_1, 0))    
        self.connect((self.baz_udp_source_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_interleaved_short_to_complex_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.facsink_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.wxgui_waterfallsink2_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.wxgui_constellationsink2_0, 0))    

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.set_samp_rate(self.adc_rate/self.decim)

    def get_config_xlate_offset(self):
        return self.config_xlate_offset

    def set_config_xlate_offset(self, config_xlate_offset):
        self.config_xlate_offset = config_xlate_offset
        self.set_xlate_offset(self.config_xlate_offset)

    def get_adc_rate(self):
        return self.adc_rate

    def set_adc_rate(self, adc_rate):
        self.adc_rate = adc_rate
        self.set_samp_rate(self.adc_rate/self.decim)

    def get_xlate_offset_fine(self):
        return self.xlate_offset_fine

    def set_xlate_offset_fine(self, xlate_offset_fine):
        self.xlate_offset_fine = xlate_offset_fine
        self._xlate_offset_fine_slider.set_value(self.xlate_offset_fine)
        self._xlate_offset_fine_text_box.set_value(self.xlate_offset_fine)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.xlate_offset+self.xlate_offset_fine)

    def get_xlate_offset(self):
        return self.xlate_offset

    def set_xlate_offset(self, xlate_offset):
        self.xlate_offset = xlate_offset
        self._config_xlate_offset_config = ConfigParser.ConfigParser()
        self._config_xlate_offset_config.read(".grc_udp_fac")
        if not self._config_xlate_offset_config.has_section("main"):
        	self._config_xlate_offset_config.add_section("main")
        self._config_xlate_offset_config.set("main", "xlate_offset", str(self.xlate_offset))
        self._config_xlate_offset_config.write(open(".grc_udp_fac", 'w'))
        self._xlate_offset_text_box.set_value(self.xlate_offset)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.xlate_offset+self.xlate_offset_fine)

    def get_xlate_decim(self):
        return self.xlate_decim

    def set_xlate_decim(self, xlate_decim):
        self.xlate_decim = xlate_decim

    def get_xlate_bandwidth(self):
        return self.xlate_bandwidth

    def set_xlate_bandwidth(self, xlate_bandwidth):
        self.xlate_bandwidth = xlate_bandwidth
        self._config_xlate_bandwidth_config = ConfigParser.ConfigParser()
        self._config_xlate_bandwidth_config.read(".grc_udp_fac")
        if not self._config_xlate_bandwidth_config.has_section("main"):
        	self._config_xlate_bandwidth_config.add_section("main")
        self._config_xlate_bandwidth_config.set("main", "xlate_bandwidth", str(self.xlate_bandwidth))
        self._config_xlate_bandwidth_config.write(open(".grc_udp_fac", 'w'))
        self._xlate_bandwidth_slider.set_value(self.xlate_bandwidth)
        self._xlate_bandwidth_text_box.set_value(self.xlate_bandwidth)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, self.xlate_bandwidth/2, 1000)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.facsink_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, self.xlate_bandwidth/2, 1000)))

    def get_config_xlate_bandwidth(self):
        return self.config_xlate_bandwidth

    def set_config_xlate_bandwidth(self, config_xlate_bandwidth):
        self.config_xlate_bandwidth = config_xlate_bandwidth

    def get_baseband_rate(self):
        return self.baseband_rate

    def set_baseband_rate(self, baseband_rate):
        self.baseband_rate = baseband_rate
        self._baseband_rate_static_text.set_value(self.baseband_rate)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
