class Gene:
    @classmethod
    def from_hex(cls, hex_value: str):
        # Check if hex_value is a valid hexadecimal number
        try:
            int(hex_value, 16)
        except ValueError as e:
            raise ValueError(f"{hex_value} is not a valid hexadecimal number") from e

        # Check if gene is too long (more than 32 bits)
        if len(bin(int(hex_value, 16))[2:]) > 32:
            raise ValueError(f"{hex_value} is too long for a gene (more than 32 bits)")

        instance = cls()
        instance.value = hex_value
        return instance

    @classmethod
    def from_binary(cls, binary_string: str):
        try:
            hex_value = hex(int(binary_string, 2))[
                2:
            ]  # convert binary to hex and remove '0x' prefix
        except ValueError as e:
            raise ValueError(f"{binary_string} is not a valid binary number") from e

        return cls.from_hex(hex_value)

    def to_binary(self) -> str:
        return bin(int(self.value, 16))[2:].zfill(32)

    def to_hex(self) -> str:
        return self.value

    def parse(
        self,
        num_sensory_neurons: int,
        num_internal_neurons: int,
        num_action_neurons: int,
    ):
        # Check if there are more neurons than can be addressed with 8 bits
        if any(
            x > 256
            for x in [num_sensory_neurons, num_internal_neurons, num_action_neurons]
        ):
            raise ValueError("Number of neurons cannot be more than 256")

        binary = self.to_binary()
        source_type = int(binary[0], 2)
        source_id = int(binary[1:9], 2) % (
            num_sensory_neurons if source_type == 0 else num_internal_neurons
        )

        sink_type = int(binary[9], 2)
        sink_id = int(binary[10:18], 2) % (
            num_internal_neurons if sink_type == 0 else num_action_neurons
        )

        weight = int(binary[18:], 2) / (2**12 - 1) * 8 - 4  # scale to [-4, 4]

        return {
            "source_type": "sensory" if source_type == 0 else "internal",
            "source_id": source_id,
            "sink_type": "internal" if sink_type == 0 else "action",
            "sink_id": sink_id,
            "weight": weight,
        }
