import pandas as pd

def loadCSV(csv1, csv2):
    # Read CSV's -> DataFrames
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)
    compareCSV(df1, df2)
    return df1, df2

def compareCSV(df1, df2):
    # Compare CSV's
    print("Comparing CSV's...")
    # Compare Columns
    if df1.columns.all() == df2.columns.all():
        print("Columns are the same.")
    else:
        print("Columns are different.")
    # Compare Rows
    # Find common rows regardless of their positions
    common_rows = set(map(tuple, df1.values)) & set(map(tuple, df2.values))
    sim = pd.DataFrame(list(common_rows), columns=df1.columns)
    print("Similarities:")
    print(sim)
    
    # Find rows in df1 that are not in df2
    diff = df1[~df1.apply(tuple, 1).isin(df2.apply(tuple,1))]
    print("Differences:")
    print(diff)
    # Ask to Save
    choice = input("Would you like to save the differences and similarities? (y/n): ")
    if choice == "y":
        saveCSV(diff, sim)
    else:
        print("Thank you for using CSV Comp.")

def saveCSV(diff, sim):
    # Save Differences
    diff.to_csv("differences.csv", index=False)
    print("Differences have been saved as differences.csv")
    # Save Similarities
    sim.to_csv("similarities.csv", index=False)
    print("Similarities have been saved as similarities.csv")
    print("Thank you for using CSV Comp.")

def main():
    # Welcome Message
    print("Welcome to CSV Comp. A tool to Compare two CSV's and find the differences / similarities between them.")
    # Get Path Input
    csv1Path = input("Enter the path of the first CSV: ")
    csv2Path = input("Enter the path of the second CSV: ")
    print("Loading CSV's...")
    loadCSV(csv1Path, csv2Path) 

if __name__ == "__main__":
    main()
