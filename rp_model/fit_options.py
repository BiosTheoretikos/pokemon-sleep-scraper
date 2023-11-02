from types import SimpleNamespace

from rp_model.utils.rounding import RoundApprox, soft_round_options

fit_options = SimpleNamespace(
    data_file="./data/rp_model/data/rp-data.pickle",
    result_file=lambda hash_id: f"./data/rp_model/results/least-squares-fit-{hash_id}.pickle",
    least_squares_kwargs=dict(loss="huber", xtol=None, verbose=2, max_nfev=200, f_scale=10),
    bonus_rounding=RoundApprox.Exact,
    rp_rounding=RoundApprox.Pass,
    soft_round=soft_round_options,
)

# Option 1
# bonus_rounding = RoundApprox.Soft,
# rp_rounding = RoundApprox.Soft

# Option 2
# bonus_rounding = RoundApprox.Exact,
# rp_rounding = RoundApprox.Pass
