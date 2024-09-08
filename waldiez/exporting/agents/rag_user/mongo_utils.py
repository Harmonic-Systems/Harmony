"""Get mongodb related content and imports."""

from typing import Set, Tuple

from harmony.models import WaldieRagUser


def _get_mongodb_embedding_function_string(
    agent: WaldieRagUser, agent_name: str
) -> Tuple[str, str, str]:
    """Get the MongoDBAtlasVectorDB embedding function string.

    Parameters
    ----------
    agent : WaldieRagUser
        The agent.
    agent_name : str
        The agent's name.

    Returns
    -------
    Tuple[str, str, str]
        The 'embedding_function', the import and the custom_embedding_function.
    """
    to_import = ""
    embedding_function_arg = ""
    embedding_function_body = ""
    if not agent.retrieve_config.use_custom_embedding:
        to_import = "from sentence_transformers import SentenceTransformer"
        embedding_function_arg = (
            "SentenceTransformer("
            f'"{agent.retrieve_config.db_config.model}"'
            ").encode"
        )
    else:
        embedding_function_arg = f"custom_embedding_function_{agent_name}"
        embedding_function_body = (
            f"\ndef custom_embedding_function_{agent_name}():\n"
            f"{agent.retrieve_config.embedding_function_string}\n"
        )
    return embedding_function_arg, to_import, embedding_function_body


def get_mongodb_db_args(
    agent: WaldieRagUser, agent_name: str
) -> Tuple[str, Set[str], str]:
    """Get the kwargs to use for MongoDBAtlasVectorDB.

    Parameters
    ----------
    agent : WaldieRagUser
        The agent.
    agent_name : str
        The agent's name.

    Returns
    -------
    Tuple[str, Set[str], str]
        The kwargs to use, what to import and the custom_embedding_function.
    """
    embedding_function_arg, to_import_embedding, embedding_function_body = (
        _get_mongodb_embedding_function_string(agent, agent_name)
    )
    to_import: Set[str] = (
        set() if not to_import_embedding else {to_import_embedding}
    )
    tab = " " * 12
    db_config = agent.retrieve_config.db_config
    kwarg_string = (
        f'{tab}connection_string="{db_config.connection_url}",\n'
        f"{tab}embedding_function={embedding_function_arg},\n"
    )
    wait_until_document_ready = db_config.wait_until_document_ready
    wait_until_index_ready = db_config.wait_until_index_ready
    if wait_until_document_ready is not None:
        kwarg_string += (
            f"{tab}wait_until_document_ready={wait_until_document_ready},\n"
        )
    if wait_until_index_ready is not None:
        kwarg_string += (
            f"{tab}wait_until_index_ready={wait_until_index_ready},\n"
        )
    return kwarg_string, to_import, embedding_function_body
