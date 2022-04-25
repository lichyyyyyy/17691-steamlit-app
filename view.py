import model


class View:
    cm = [[]]
    e_value = 0
    alternative = ""
    p_botrytis = 0.1
    p_no_sugar = 0.6
    p_typical_sugar = 0.3
    p_high_sugar = 0.1

    def __init__ (self):
        self.cm = model.process()
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

        ev_ns = (self.p_no_sugar * 80000 + self.p_typical_sugar * 117500 + self.p_high_sugar * 125000) * 12
        ev_s = (self.p_botrytis * 80000 + (1-self.p_botrytis) * 117500) * 12
        ev_h = 80000 * 12

        self.e_value = p_dns * (p_ns_dns*ev_ns + (1-p_ns_dns)*ev_s) + p_ds * (p_s_ds*ev_s + (1-p_s_ds)*ev_ns)

        if self.e_value > ev_h:
            self.alternative = "Keep waiting"
        else:
            self.alternative = "Harvest now"


