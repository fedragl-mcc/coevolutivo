import numpy as np
def topsis(population,weights=None,shared=False): 
    chromosomes = population[0]
    if shared:
        del population[-1]
    criteria = np.array(population[1:])

    # transpose: rows = individuals, cols = criteria
    decision_matrix = criteria.T  
    
    n_individuals, n_criteria = decision_matrix.shape
    
    # default: equal weights
    if weights is None:
        weights = np.ones(n_criteria) / n_criteria
    else:
        weights = np.array(weights) / np.sum(weights)

    # # Step 1: Normalize
    # norm = np.sqrt((decision_matrix**2).sum(axis=0))
    # norm_matrix = decision_matrix / norm
    
    # Step 2: Weighted normalized
    weighted_matrix = decision_matrix * weights
    
    # Step 3: Ideal best and worst (all are benefits here)
    ideal_best = weighted_matrix.max(axis=0)
    ideal_worst = weighted_matrix.min(axis=0)
    
    # Step 4: Distances
    dist_best = np.sqrt(((weighted_matrix - ideal_best)**2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_matrix - ideal_worst)**2).sum(axis=1))
    
    # Step 5: Closeness coefficient
    scores = dist_worst / (dist_best + dist_worst)
    
    # Rank individuals
    ranking = np.argsort(-scores)  # descending
    
    # ---- Rebuild population in ranked order ----
    ranked_population = []
    for row in population:
        ranked_population.append([row[i] for i in ranking])

    # # Optionally, you can append the scores as a new row
    # ranked_population.append([scores[i] for i in ranking])
    return ranked_population