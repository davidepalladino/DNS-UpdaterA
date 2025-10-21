class RecordDTO:
    """
    Data Transfer Object (DTO) representing a DNS record.
    """

    _id: str
    _name: str
    _ip: str

    def __init__(self, id: str, name: str, ip: str):
        """
        Initializes a RecordDTO instance.

        Args:
            id: The ID of the DNS record.
            name: The name of the DNS record.
            ip: The IP address associated with the DNS record.
        """
        self._id = id
        self._name = name
        self._ip = ip

    def get_id(self) -> str:
        """
        Returns the ID of the DNS record.

        Returns:
            The ID of the DNS record.
        """
        return self._id

    def get_name(self) -> str:
        """
        Returns the name of the DNS record.

        Returns:
            The name of the DNS record.
        """
        return self._name

    def get_ip(self) -> str:
        """
        Returns the IP address associated with the DNS record.

        Returns:
            The IP address associated with the DNS record.
        """
        return self._ip


class ResultUpdateDTO:
    """
    Data Transfer Object (DTO) representing the result of an update operation.
    """

    _state: bool
    _reason: str

    def __init__(self, state: bool, reason: str):
        """
        Initializes a ResultUpdateDTO instance.

        Args:
            state: A boolean indicating whether the update was successful.
            reason: A string explaining the reason for the update state.
        """
        self._state = state
        self._reason = reason

    def get_state(self) -> bool:
        """
        Returns the state of the update operation.

        Returns:
            True if the update was successful, False otherwise.
        """
        return self._state

    def get_reason(self) -> str:
        """
        Returns the reason for the update state.

        Returns:
            A string explaining the reason for the update state.
        """
        return self._reason