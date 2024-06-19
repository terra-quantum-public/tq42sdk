import pytest

from tq42.dataset import Dataset, StorageProto


def test__get_file_name_from_signed_url():
    signed_url = "https://storage.googleapis.com/random-uuid-that-is-not-valid/photovoltaic_data_units_no_label.xlsx?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=not-valid-cred%40service-account-uri&X-Goog-Date=20240619T071407Z&X-Goog-Expires=900&X-Goog-SignedHeaders=host&X-Goog-Signature=some-random-signature-thingy-with-random-numbers-123913-1240235"
    file_name = Dataset._get_file_name_from_signed_url(signed_url)
    assert file_name == "photovoltaic_data_units_no_label.xlsx"


def test__get_file_name_from_signed_url_no_params():
    signed_url = "https://storage.googleapis.com/random-uuid-that-is-not-valid/photovoltaic_data_units_no_label.xlsx"
    file_name = Dataset._get_file_name_from_signed_url(signed_url)
    assert file_name == "photovoltaic_data_units_no_label.xlsx"


def test__get_file_name_from_signed_url_no_file_ending():
    signed_url = "https://storage.googleapis.com/random-uuid-that-is-not-valid/photovoltaic_data_units_no_label?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=not-valid-cred%40service-account-uri&X-Goog-Date=20240619T071407Z&X-Goog-Expires=900&X-Goog-SignedHeaders=host&X-Goog-Signature=some-random-signature-thingy-with-random-numbers-123913-1240235"
    file_name = Dataset._get_file_name_from_signed_url(signed_url)
    assert file_name == "photovoltaic_data_units_no_label"


def test__get_file_name_from_signed_url_no_valid_url():
    signed_url = "hps://storage/random-uuid-that-is-not-valid/photo"

    with pytest.raises(ValueError):
        Dataset._get_file_name_from_signed_url(signed_url)


def test_dataset_export_non_valid_directory():
    data = StorageProto(
        id="83976d81-ffaa-4778-b894-89ca8d5801f2",
        name="pseudo-dataset-data",
    )
    dataset = Dataset.from_proto(client={}, msg=data)
    with pytest.raises(ValueError):
        dataset.export(directory_path="/Users/definitely-not-a-valid-user/directory")
