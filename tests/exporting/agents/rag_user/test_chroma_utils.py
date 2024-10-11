"""Test harmony.exporting.agents.rag_user.chroma_utils.*."""

import os

from harmony.exporting.agents.rag_user.chroma_utils import get_chroma_db_args
from harmony.models import (
    WaldieRagUser,
    WaldieRagUserData,
    WaldieRagUserRetrieveConfig,
    WaldieRagUserVectorDbConfig,
)

# pylint: disable=line-too-long


def test_get_chroma_db_args() -> None:
    """Test get_chroma_db_args."""
    # Given
    rag_user = WaldieRagUser(
        id="wa-1",
        name="rag_user",
        type="agent",
        agent_type="rag_user",
        description="description",
        tags=["tag1"],
        requirements=["requirement1"],
        data=WaldieRagUserData(  # type: ignore
            retrieve_config=WaldieRagUserRetrieveConfig(  # type: ignore
                docs_path="docs_path",
                collection_name="collection_name",
                get_or_create=True,
                vector_db="chroma",
                db_config=WaldieRagUserVectorDbConfig(  # type: ignore
                    use_local_storage=True,
                    local_storage_path="local_storage_path",
                    model="model",
                ),
                use_custom_embedding=False,
            ),
        ),
    )
    agent_name = "rag_user"
    # When
    kwargs, imports, embeddings_func, before = get_chroma_db_args(
        rag_user, agent_name
    )
    # Then
    local_path = os.path.join(os.getcwd(), "local_storage_path")
    assert kwargs == (
        f'            client=chromadb.PersistentClient(path="{local_path}"),\n'
        '            embedding_function=SentenceTransformerEmbeddingFunction(model_name="model"),\n'
    )
    assert embeddings_func == ""
    assert imports == {
        "chromadb",
        "from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction",
    }
    assert before == (
        f'rag_user_client = chromadb.PersistentClient(path="{local_path}")\n'
        'rag_user_client.get_or_create_collection("collection_name")\n'
    )


def test_get_chroma_db_args_no_local() -> None:
    """Test get_chroma_db_args with no local storage."""
    # Given
    rag_user = WaldieRagUser(
        id="wa-1",
        name="rag_user",
        type="agent",
        agent_type="rag_user",
        description="description of rag_user",
        tags=["tag3"],
        requirements=["requirement4", "requirement5"],
        data=WaldieRagUserData(  # type: ignore
            retrieve_config=WaldieRagUserRetrieveConfig(  # type: ignore
                docs_path="docs_path",
                collection_name="collection_name",
                vector_db="chroma",
                db_config=WaldieRagUserVectorDbConfig(  # type: ignore
                    use_local_storage=False,
                    local_storage_path=None,
                    model="model",
                ),
                use_custom_embedding=False,
            ),
        ),
    )
    agent_name = "rag_user"
    # When
    kwargs, imports, embeddings_func, _ = get_chroma_db_args(
        rag_user, agent_name
    )
    # Then
    assert kwargs == (
        "            client=chromadb.Client(),\n"
        '            embedding_function=SentenceTransformerEmbeddingFunction(model_name="model"),\n'
    )
    assert embeddings_func == ""
    assert imports == {
        "chromadb",
        "from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction",
    }


def test_get_chroma_db_custom_embeddings() -> None:
    """Test get_chroma_db_args with custom embeddings."""
    # Given
    custom_embedding = (
        "def custom_embedding_function():\n"
        '    return SentenceTransformerEmbeddingFunction(model_name="model")\n'
    )
    rag_user = WaldieRagUser(
        id="wa-1",
        name="rag_user",
        type="agent",
        agent_type="rag_user",
        description="description",
        tags=["tag2"],
        requirements=["requirement4"],
        data=WaldieRagUserData(  # type: ignore
            retrieve_config=WaldieRagUserRetrieveConfig(  # type: ignore
                docs_path="docs_path",
                collection_name="collection_name",
                vector_db="chroma",
                db_config=WaldieRagUserVectorDbConfig(  # type: ignore
                    use_local_storage=False,
                    local_storage_path=None,
                    model="model",
                ),
                use_custom_embedding=True,
                embedding_function=custom_embedding,
            ),
        ),
    )
    agent_name = "rag_user"
    # When
    kwargs, imports, embeddings_func, _ = get_chroma_db_args(
        rag_user, agent_name
    )
    # Then
    assert kwargs == (
        "            client=chromadb.Client(),\n"
        "            embedding_function=custom_embedding_function_rag_user,\n"
    )
    assert embeddings_func == (
        "\ndef custom_embedding_function_rag_user():\n"
        "    # type: () -> Callable[..., Any]\n"
        '    return SentenceTransformerEmbeddingFunction(model_name="model")\n'
    )
    assert imports == {"chromadb"}
