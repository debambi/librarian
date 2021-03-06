import logging

from bottle import request
from bottle_utils.i18n import lazy_gettext as _

from ..forms import ondd as ondd_forms
from ..helpers import ondd as ondd_helpers


def get_form():
    """
    Return appropriate form class for configured frequency band
    """
    return ondd_forms.FORMS[ondd_helpers.get_band()]


class ONDDStep:
    name = 'ondd'
    index = 30
    template = 'setup/step_ondd.tpl'

    @staticmethod
    def test():
        ondd_client = request.app.supervisor.exts.ondd
        ondd_alive = ondd_client.ping()
        if not ondd_alive:
            # If ondd is not running, skip the step
            return False
        settings = ondd_helpers.read_ondd_setup()
        if settings is None:
            # Settings is None if ONDD configuration has never been performed
            return True
        # If there is any ondd configuration stored, even if it's just empty
        # which could mean the user skipped that step, don't invoke it again
        return False

    @staticmethod
    def get():
        ondd_client = request.app.supervisor.exts.ondd
        snr_min = request.app.config.get('ondd.snr_min', 0.2)
        snr_max = request.app.config.get('ondd.snr_max', 0.9)
        ONDDForm = get_form()
        band = ondd_helpers.get_band()
        return dict(status=ondd_client.get_status(),
                    band=band,
                    lband=ondd_helpers.LBAND,
                    kuband=ondd_helpers.KUBAND,
                    is_l=band == ondd_helpers.LBAND,
                    is_ku=band == ondd_helpers.KUBAND,
                    preset_keys=ONDDForm.PRESETS[0].values.keys(),
                    form=ONDDForm(),
                    SNR_MIN=snr_min,
                    SNR_MAX=snr_max)

    @staticmethod
    def post():
        ondd_client = request.app.supervisor.exts.ondd
        is_test_mode = request.forms.get('mode', 'submit') == 'test'
        ONDDForm = get_form()
        form = ONDDForm(request.forms)
        form_valid = form.is_valid()
        snr_min = request.app.config.get('ondd.snr_min', 0.2)
        snr_max = request.app.config.get('ondd.snr_max', 0.9)
        band = ondd_helpers.get_band()

        if form_valid:
            # Store full settings
            logging.info('ONDD: tuner settings updated')
            ondd_helpers.write_ondd_setup(form.processed_data)
            if is_test_mode:
                return dict(successful=False,
                            form=form,
                            status=ondd_client.get_status(),
                            # Translators, shown when tuner settings are
                            # updated during setup wizard step.
                            message=_('Tuner settings have been updated'),
                            band=band,
                            lband=ondd_helpers.LBAND,
                            kuband=ondd_helpers.KUBAND,
                            is_l=band == ondd_helpers.LBAND,
                            is_ku=band == ondd_helpers.KUBAND,
                            preset_keys=ONDDForm.PRESETS[0].values.keys(),
                            SNR_MIN=snr_min,
                            SNR_MAX=snr_max)
            return dict(successful=True)
        # Form is not valid
        if is_test_mode:
            # We only do something about this in test mode
            return dict(successful=False,
                        form=form,
                        status=ondd_client.get_status(),
                        band=band,
                        lband=ondd_helpers.LBAND,
                        kuband=ondd_helpers.KUBAND,
                        is_l=band == ondd_helpers.LBAND,
                        is_ku=band == ondd_helpers.KUBAND,
                        preset_keys=ONDDForm.PRESETS[0].values.keys(),
                        SNR_MIN=snr_min,
                        SNR_MAX=snr_max)

        ondd_helpers.write_ondd_setup({})
        return dict(successful=True)
