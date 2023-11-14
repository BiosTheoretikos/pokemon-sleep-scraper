from calc.rp_model import get_rp_model_result


def get_rp_model_df():
    return get_rp_model_result("results/{hash_id}.pickle")
