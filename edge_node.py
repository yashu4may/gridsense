# Array to track how many times EVERY house (1 to 50) has been shut down
cut_counts = {i: 0 for i in range(1, 51)}

def check_and_act(predicted_load):
    """
    Checks if load is > 100.
    If yes, finds the house with the lowest cut count to be fair.
    """
    if predicted_load > 100.0:
        # Find the house ID that has been cut the LEAST amount of times
        house_to_cut = min(cut_counts, key=cut_counts.get)

        # Increase their cut count tally
        cut_counts[house_to_cut] += 1

        # Return the target house
        return house_to_cut

    return None  # Grid is safe