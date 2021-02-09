class Log:
    def __init__(
        self,
        log_id=None,
        is_to_update=False,
        action_msg="",
        nbr_of_action_errors=0,
        log_datetime_start=None,
        log_datetime_end=None,
        fk_status_id=None,
        is_alert_on=False,
        fk_batch_id=None,
        fk_metadata_id=None,
        is_stored_in_db=None,
        fk_action_status_id=1,
        fk_download_status_id=None,
        fk_handling_status_id=None,
        ):
        self.log_id = log_id
        self.is_to_update = is_to_update
        self.action_msg = action_msg
        self.nbr_of_action_errors = nbr_of_action_errors
        self.log_datetime_start = log_datetime_start
        self.log_datetime_end = log_datetime_end
        self.fk_status_id = fk_status_id
        self.is_alert_on = is_alert_on
        self.fk_batch_id = fk_batch_id
        self.fk_metadata_id = fk_metadata_id
        self.is_stored_in_db = is_stored_in_db
        self.fk_action_status_id = fk_action_status_id
        self.fk_download_status_id = fk_download_status_id
        self.fk_handling_status_id = fk_handling_status_id