"""Test harmony.io_stream.*."""

from harmony.io import HarmonyIOStream


def test_harmony_io_stream() -> None:
    """Test HarmonyIOStream."""
    # Given

    input_prompt = ""

    def on_prompt_input(prompt: str) -> None:
        """On prompt input.

        Parameters
        ----------
        prompt : str
            The prompt.
        """
        # A more realistic example would be to send the prompt to a websocket
        # and when the user sends the input, we would call
        # `harmony_io_stream.forward_input(input_data)` with the input data.
        nonlocal input_prompt
        input_prompt = prompt

    harmony_io_stream = HarmonyIOStream(
        print_function=print,
        on_prompt_input=on_prompt_input,
        input_timeout=2,
    )

    # when
    with HarmonyIOStream.set_default(harmony_io_stream):
        # then
        harmony_io_stream.print("print")
        assert input_prompt == ""
        harmony_io_stream.forward_input("User's input")
        users_input = harmony_io_stream.input(">")
        assert users_input == "User's input"
        assert input_prompt == "Your input:"

    harmony_io_stream.close()


def test_reuse_harmony_io_stream() -> None:
    """Test reusing HarmonyIOStream."""
    # Given
    harmony_io_stream = HarmonyIOStream(print_function=print, input_timeout=1.1)

    # when
    with HarmonyIOStream.set_default(harmony_io_stream):
        # then
        harmony_io_stream.print("print")
        users_input = harmony_io_stream.input(">")
        assert users_input == "\n"
    harmony_io_stream.close()
    # re open
    harmony_io_stream.open()
    with HarmonyIOStream.set_default(harmony_io_stream):
        harmony_io_stream.print("print")
        users_input = harmony_io_stream.input(">")
        assert users_input == "\n"
    harmony_io_stream.close()


def test_harmony_io_stream_no_input() -> None:
    """Test HarmonyIOStream without an input value."""
    # Given
    harmony_io_stream = HarmonyIOStream(print_function=print, input_timeout=1.1)

    # when
    with HarmonyIOStream.set_default(harmony_io_stream):
        # then
        harmony_io_stream.print("print")
        users_input = harmony_io_stream.input("Enter something:")
        assert users_input == "\n"
