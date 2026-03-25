from src.data_generation.generator import LoanDataGenerator
import os

# Generating the Raw Data

if __name__ == "__main__":

    # Ensure the raw data directory exists
    os.makedirs("data/raw", exist_ok=True)
    
    # Initialize the generator (let's start with 500 loans for testing)
    generator = LoanDataGenerator(10000)
    
    # Generate and save the data
    generator.generate_and_save(raw_data_path="data/raw")

#---------------------------------------------------------------------------------------------------------------

