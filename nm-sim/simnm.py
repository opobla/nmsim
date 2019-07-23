from numpy.random import exponential
from decimal import *
import math


class CounterTube(object):
    def __init__(self, channel, beta, pulse_width=22e-6):
        self.pulse_width = Decimal(pulse_width)
        self.output_state = 0
        self.pulse_deactivation_time = None
        self.beta = beta
        self._id = channel
        self._current_time = Decimal(0)
        self._next_particle_event = Decimal(exponential(beta))

    @property
    def id(self):
        return self._id

    @property
    def next_event(self):
        return self._next_particle_event if not self.pulse_deactivation_time else \
            min(self._next_particle_event, self.pulse_deactivation_time)

    @property
    def current_time(self):
        return self._current_time

    @current_time.setter
    def current_time(self, current_time):
        self._current_time = current_time
        if current_time >= self._next_particle_event:
            self._next_particle_event = current_time + Decimal(exponential(self.beta))
            self.enable_output_pulse()

        if self.pulse_deactivation_time and self.pulse_deactivation_time <= self._current_time:
            self.disable_output_pulse()

    def enable_output_pulse(self):
        if self.output_state == 0:
            self.output_state = 1
            self.pulse_deactivation_time = self.current_time + self.pulse_width

    def disable_output_pulse(self):
        self.output_state = 0
        self.pulse_deactivation_time = None


class NeutronMonitor(object):
    def __init__(self, size, beta):
        self.beta = beta
        self.size = size
        self.counter_list = []
        self._current_time = Decimal(0)

        for i in range(size):
            self.counter_list.append(CounterTube(i, beta))

    def get_next_sim_event(self):
        while True:
            data = [t.next_event for t in self.counter_list]
            yield min(data)

    @property
    def status(self):
        return [counter.output_state for counter in self.counter_list]

    @property
    def current_time(self):
        return self._current_time

    @current_time.setter
    def current_time(self, current_sim_time_sec):
        self._current_time = current_sim_time_sec
        for counter in self.counter_list:
            counter.current_time = current_sim_time_sec


class Sampler:
    counter: int
    neutron_monitor: NeutronMonitor

    def __init__(self, sampling_period_s, neutron_monitor):
        self.counter = 0
        self.current_sim_sampler_time_sec = Decimal(0)
        self.neutron_monitor = neutron_monitor
        self.sampling_period_s = sampling_period_s

    def generator(self, limit_time_s):
        next_sim_event_time_s = next(self.neutron_monitor.get_next_sim_event())

        while next_sim_event_time_s < limit_time_s:
            last_sim_event_time_s = next_sim_event_time_s
            next_sim_event_time_s = next(self.neutron_monitor.get_next_sim_event())

            delta = math.ceil((next_sim_event_time_s - last_sim_event_time_s) / self.sampling_period_s)
            self.counter = self.counter + delta
            self.neutron_monitor.current_time = next_sim_event_time_s

            status_bin = ""
            for channel in self.neutron_monitor.status:
                if channel == 0:
                    status_bin = status_bin + "0"
                else:
                    status_bin = status_bin + "1"

            yield {'delta_steps': delta, 'counter_steps': self.counter, 'time_s': next_sim_event_time_s,
                   'status_bin': status_bin}
