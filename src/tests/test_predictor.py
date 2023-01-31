import joblib


def test_estimate_wine_quality(app_client, test_auth, test_model_path, mocker):
    # given
    endpoint = "/wine/quality"
    url_params = "fixed_acidity=4.6&volatile_acidity=0.12&citric_acid=0.0&residual_sugar=0.9&chlorides=0.012&free_sulfur_dioxide=1.0&total_sulfur_dioxide=6.0&density=0.99007&ph=2.74&sulphates=0.33&alcohol=8.4"

    mocker.patch("wine_predictor_api.services.predictor.load_model",
                 return_value=joblib.load(test_model_path), autospec=True)

    # when
    response = app_client.get(f"{endpoint}?{url_params}", headers={"Authorization": test_auth})

    # then
    assert response.status_code == 200
    assert response.json.get("estimation") == 6
