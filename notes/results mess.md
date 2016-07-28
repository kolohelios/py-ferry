by working backwards:

Financial_Calc should return an array of "ferry informations", or metadata that is associated with a ferry that includes properties that relate to the turn results for each ferry

[
    {
        ferry: ferry object
        results: {
            fuel_used: ...
            total_passengers: ...
        }
    }
]

results are based on calculations performed for each day within the week
so, Financial_Calc().calc_weekly_results_for_route() seems like an unnecessary indirection in hindsight

sailings will need to take data for days and accumulate it with a ferry; passing these relatively complex arrays of objects between functions is a mess and is almost certiainly not necessary