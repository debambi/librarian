from greentasks import Task
from ondd_ipc import consts as c_ondd

from ..core.exts import ext_container as exts


_ = lambda x: x


class ONDDQueryTask(Task):
    name = 'ondd'
    periodic = True

    #: Maximum signal strength usable by the indicator
    MAX_STRENGTH = 4

    def get_start_delay(self):
        return exts.config['ondd.refresh_rate']

    def get_delay(self, previous_delay):
        return exts.config['ondd.refresh_rate']

    def send_cache_warning(self):
        db = exts.databases.librarian
        exts.notifications.send(
            # Translators, notification displayed when internal cache storage
            # is running out of disk space
            _('Download capacity is getting low. '
              'Please ask the administrator to take action.'),
            category='ondd_cache',
            dismissable=False,
            priority=exts.notifications.CRITICAL,
            group='guest',
            db=db)
        exts.notifications.send(
            # Translators, notification displayed when internal cache storage
            # is running out of disk space
            _('Download cache capacity is getting low. You will stop receiving'
              ' new content if you run out of storage space. Please move some '
              'content from the internal storage to an external one.'),
            category='ondd_cache',
            dismissable=False,
            priority=exts.notifications.CRITICAL,
            group='superuser',
            db=db)

    def query_cache(self):
        """
        Return the post-processed values of ondd cache status information.
        """
        cache_min = exts.config['ondd.cache_min']
        cache_max = exts.config['ondd.cache_quota']
        cache_status = exts.ondd.get_cache_storage()
        real_free = cache_status['free']
        real_used = cache_status['used']
        cache_critical = real_free < cache_min

        # First of all, since used space is real, but capacity is virtual
        # (cache_max), we need to make sure used space does not exceed the
        # capacity, or we'll get weird results.
        cache_used = min(real_used, cache_max)

        # We want cache to be a certain amount (cache_max). Since this is a
        # virtual capacity, we also have a virtual free space which is the
        # amount of space we want the cache to have (ideally) and the amount
        # of data used in reality.
        virt_free = cache_max - cache_used

        # ONDD download cache is shared with other data that is stored on the
        # internal disk. This includes databases, logs, and downloaded files
        # that are not part of the cache (permanent files). The foreign data
        # may actually bite into the cache space. In this case, we need to add
        # to the used space, and subtract from the virtual free space.
        cache_foreign = abs(min(0, real_free - virt_free))
        cache_used += cache_foreign
        virt_free -= cache_foreign

        # Sanity check
        assert virt_free + cache_used == cache_max

        # First clean any notifications
        db = exts.databases.librarian
        exts.notifications.delete_by_category('ondd_cache', db)

        if cache_critical:
            # Now we also need to warn the user about low cache capacity
            self.send_cache_warning()

        return dict(total=cache_max,
                    free=virt_free,
                    used=cache_used,
                    alert=cache_critical)

    def query_status(self):
        """
        Return the raw status data obtained from the ondd endpoint as-is, only
        extended with librarian's interpretation of the signal strength, based
        on the values that it got.
        """
        status = exts.ondd.get_status()
        sig_state = status['state']
        is_receiving = any(strm['bitrate'] > 0 for strm in status['streams'])
        # dividing the raw snr value by two gives us a value between 0 and 4,
        # which is the range of acceptable values for the indicator, with 4
        # being max strength that translates into "full"
        # in case it exceeds 4, it will just use the max value
        strength = min(int(status['snr'] / 2), self.MAX_STRENGTH)
        if strength == self.MAX_STRENGTH:
            strength = 'full'
        middle = '-{strength}'.format(strength=strength)
        state_lut = {
            c_ondd.STATE_SEARCH: '-search',
            c_ondd.STATE_SIGDET: '-detect',
            c_ondd.STATE_CONST_LOCK: middle,
            c_ondd.STATE_CODE_LOCK: middle + '-lock',
            c_ondd.STATE_FRAME_LOCK: middle + ('-lock', '-recv')[is_receiving],
        }
        # this results in a string such as "-2-recv", "-1-lock", etc or in case
        # there is no usable signal it's just "-search" or "-detect"
        status.update(indicator=state_lut[sig_state])
        return status

    def query_transfers(self):
        """
        Return the active transfers as reported by the ondd endpoint.
        """
        return exts.ondd.get_transfers()

    def run(self):
        cache = self.query_cache()
        status = self.query_status()
        transfers = self.query_transfers()
        # update global state through provider
        data = dict(cache=cache,
                    status=status,
                    transfers=transfers)
        provider = exts.state.provider('ondd')
        provider.set(data)

