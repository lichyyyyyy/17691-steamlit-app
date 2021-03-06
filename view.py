import model


class View:
    cm = [[]]
    e_value = 0
    p_botrytis = 0.1
    p_no_sugar = 0.6
    p_typical_sugar = 0.3
    p_high_sugar = 0.1
    alternative_dns = ""
    alternative_ds = ""

    def __init__ (self):
        self.cm = model.process()
        self.cm = [[9, 3], [1, 1]]
        self.calculate_e_value()
        
    def calculate_e_value(self):
        cm = self.cm
        all = cm[0][0] + cm[0][1] + cm[1][0] + cm[1][1]
        p_dns = (cm[1][0]+cm[1][1]) / all
        p_dns_ns = cm[1][1] / (cm[0][1] + cm[1][1])
        p_ns = 0.5
        p_ns_dns = p_dns_ns * p_ns / p_dns

        p_ds = (cm[0][0]+cm[0][1]) / all
        p_ds_s = cm[0][0] / (cm[0][0] + cm[1][0])
        p_s = 0.5
        p_s_ds = p_ds_s * p_s / p_ds

        # Expected value if waiting and no storm
        ev_ns = (self.p_no_sugar * 80000 + self.p_typical_sugar * 117500 + self.p_high_sugar * 125000) * 12
        # Expected value if waiting but storm
        ev_s = (self.p_botrytis * 275000 + (1-self.p_botrytis) * 35000) * 12
        # Expected value if harvesting now
        ev_h = 80000 * 12

        ev_dns_waiting = p_ns_dns*ev_ns + (1-p_ns_dns)*ev_s
        ev_ds_waiting = p_s_ds*ev_s + (1-p_s_ds)*ev_ns
        # Maxinum expected value with a detection of storm
        ev_ds = max(ev_h, ev_ds_waiting)
        # Maxinum expected value with a detection of no storm
        ev_dns = max(ev_h, ev_dns_waiting)

        # e-value 
        self.e_value = p_dns * ev_dns + p_ds * ev_ds

        if ev_ds_waiting > ev_h:
            self.alternative_ds = "keep waiting"
        else:
            self.alternative_ds = "harvest now"

        if ev_dns_waiting > ev_h:
            self.alternative_dns = "keep waiting"
        else:
            self.alternative_dns = "harvest now"

