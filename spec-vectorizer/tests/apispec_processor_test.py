import yaml
from processor.spec_split import split_openapi_spec_by_path

def test_split_openapi_spec_by_path_basic():
    try:
        with open("spec-vectorizer/tests/resources/openapi.yaml", 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file)

        result = split_openapi_spec_by_path(yaml_data=yaml_data)
        
        assert len(result) == 1
        paths = [list(r['paths'].keys())[0] for r in result]
        assert set(paths) == {'/pet'}
        for r in result:
            assert r['openapi'] == '3.0.4'
            assert 'info' in r
            assert 'servers' in r
            assert 'components' in r
    except Exception as e:
        print(e)
        assert False

def test_split_openapi_spec_by_path_missing_fields():
    try:
        with open("spec-vectorizer/tests/resources/openapi_missing_fields.yaml", 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file)

        result = split_openapi_spec_by_path(yaml_data=yaml_data)
        
        assert len(result) == 1
        r = result[0]
        assert r['openapi'] == '3.0.4'
        assert 'info' not in r
        assert 'servers' not in r
        assert 'components' not in r
        assert '/pet' in r['paths']
    except Exception as e:
        print(e)
        assert False


def test_split_openapi_spec_by_path_empty_paths():
    try:
        with open("spec-vectorizer/tests/resources/openapi_no_paths.yaml", 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file)

        result = split_openapi_spec_by_path(yaml_data=yaml_data)
        
        assert result == []
    except Exception as e:
        print(e)
        assert False

def test_split_openapi_spec_with_multiple_paths():

    try:
        with open("spec-vectorizer/tests/resources/openapi_multiple_paths.yaml", 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file)

        result = split_openapi_spec_by_path(yaml_data=yaml_data)
       
        assert len(result) == 13
    except Exception as e:
        print(e)
        assert False