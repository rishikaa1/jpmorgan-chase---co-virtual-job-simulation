import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def exercise_0(file):
    return pd.read_csv(file)

def exercise_1(df):
    return list(df)

def exercise_2(df, k):
    return df.head(k)

def exercise_3(df, k):
    return df.sample(n=k)

def exercise_4(df):
    return df['type'].unique()

def exercise_5(df):
    return df['nameDest'].value_counts().head(10)

def exercise_6(df):
    return df[df['isFraud'] == 1]

def exercise_7(df):
    df1 = df.groupby('nameOrig')['nameDest'].agg(['nunique'])
    df1.sort_values(by=('nunique'), ascending=False, inplace=True)
    return df1
    
# Visualization 1: Transaction Type Frequencies
def visual_1(df):
    def transaction_counts(df):
        return df['type'].value_counts()
    def transaction_counts_split_by_fraud(df):
       return df.groupby(['type', 'isFraud']).size()

    fig, axs = plt.subplots(2, figsize=(6,10))
    transaction_counts(df).plot(ax=axs[0], kind='bar')
    axs[0].set_title('Frequencies of Transaction Types')
    axs[0].set_xlabel('Transaction Type')
    axs[0].set_ylabel('Number of Occurences')
    transaction_counts_split_by_fraud(df).plot(ax=axs[1], kind='bar')
    axs[1].set_title('Frequencies of Transaction Types Split by Fraud')
    axs[1].set_xlabel('Transaction Type (Fraud)')
    axs[1].set_ylabel('Number of Occurences')
    fig.suptitle('Transaction Types')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    for ax in axs:
      for p in ax.patches:
          ax.annotate(p.get_height(), (p.get_x(), p.get_height()))
    print('Conclusions:')
    print('1. Transactions with Fraud Cases: CASH_OUT and TRANSFER')
    print('2. Transaction without Fraud Cases: PAYMENT, CASH_IN, DEBIT')
    print()
    print('Transaction Description based on Analysis:')
    print('1. PAYMENT Transactions: Highest transaction volumes with 73, 427 occurences. No fraud cases detected in this category, suggesting strong security measures or low interest from fraudsters.')
    print('2. CASH_OUT Transactions: 66,488 occurences with 75 fraud cases (fraud rate: 0.11%), making this transaction type prone to fraudulent activity, though the percentage is still quite low compared to the total volume.')
    print('3. CASH_IN Transactions: 41,579 occurences with no fraud cases reported, similar to PAYMENT transactions.')
    print('4. TRANSFER Transactions: 16,836 occurences with 72 fraud cases (fraud rate: 0.43%). This shows that this transaction type also poses a moderate risk for fraud.')
    print('5. DEBIT Transactions: 1,670 total occurences, the lowest among all transaction types. No fraud cases observed.')
    print()
    print('Recommendations:')
    print('1. Enhanced monitoring for CASH_OUT and TRANSFER transactions as both transaction types are vulnerable to fraud.')
    print('2. Fraud Prevention Strategies for both CASH_OUT and TRANSFER transactions. Consider adding extra authentication methods or monitoring for unusual patterns and limiting transfer sizes based on risk scoring.')
    print('3. Review and reinforce security for PAYMENT, CASH_IN and DEBIT transactions because although no fraud has been detected, it is crucial to regularly audit and update security measures to maintain their fraud-free status.')
    print('4. Given the observed fraud in CASH_OUT and TRANSFER transactions, consider integrating predictive fraud detection models based on transaction history and behavior analysis.')
    print('5. Customer education on fraudulent activities to increase awareness regarding potential fraud risks and safe transaction practices.')
    

# Visualization 2: Balance Changes in CASH_OUT Transactions
def visual_2(df):
    def query(df):
        df['Origin_Delta'] = df['oldbalanceOrg'] - df['newbalanceOrig']
        df['Destination_Delta'] = df['oldbalanceDest'] - df['newbalanceDest']
        return df[df['type'] == 'CASH_OUT']
    plot = query(df).plot.scatter(x='Origin_Delta',y='Destination_Delta')
    plot.set_title('Origin account balance delta v. Destination account balance delta scatter plot for CASH_OUT transactions')
    plot.set_xlim(left=-1e3, right=1e3)
    plot.set_ylim(bottom=-1e3, top=1e3)
    print('This scatter plot shows the relationship between changes in the origin account balance (x-axis) and the destination account balance (y-axis) for CASH_OUT transactions.')
    print()
    print('1. Expected Patterns: A diagonal pattern from (-1000, 1000) to (1000, -1000) indicates typical CASH_OUT behavior, where a decrease in the origin balance corresponds to an increase in the destination balance.')
    print('2. Cluster at (0,0): A concentration around (0,0) suggests many transactions with little or no balance change, possibly incomplete or minimal-value transactions.')
    print('3. Vertical/Horizontal Lines: These indicate cases where either the origin or destination balance remains unchanged, pointing to potential anomalies or special transaction conditions.')
    print()

# Confusion Matrix Visualization
def visual_custom(df):
    ax = plt.subplot()
    sns.heatmap(exercise_custom(df), annot=True, fmt='d', ax=ax, cmap='Blues')
    ax.set_xlabel('isFlaggedFraud')
    ax.set_ylabel('isFraud')
    ax.set_title('Confusion Matrix for Fraud Detection')
    ax.xaxis.set_ticklabels(['0', '1'])
    ax.yaxis.set_ticklabels(['0', '1'])
    plt.show()
    print('This confusion matrix provides insight into the performance of the fraud detection system.')
    print('1. True Negatives (199,853): A large number of non-fraudulent transactions were correctly classified as non-fraud, meaning the system is highly effective at identifying legitimate transactions.')
    print('2. False Negatives (147): There are 147 fraudulent transactions that were not flagged. This indicates a significant issue, as these fraudulent activites went unnoticed by the detection system. This is a critical concern for security.')
    print('3. True Positives (0): No frauduelnt transactions were correctly flagged. This means the system failed to detect any actual fraud, leading to a complete lack of fraud detection success.')
    print('4. False Positives (0): The absence of false positives is a positive outcome, meaning the system does not incorrectly flag legitimate transactions as fraudulent.')
    print()
    print('Key Insights:')
    print()
    print('1. Failure to Detect Fraud: The system has 0 true positives, showing a complete failure to catch any fraudulent transactions, raising significant concerns about the effectiveness of the fraud detection mechanism.')
    print('2. Perfect Accuracy in Non-Fraud Cases: While the system is excellent at identifying non-fraudulent transactions (high true negatives), this over-focus on avoiding false positives could come at the cost of missing fraud cases.')
    print('3. System Weakness: The confusion matrix reveals a major flaw in fraud detection, especially in scenarios where real fraud is not flagged. This suggests the system needs significant improvements, possibly by enhancing the fraud detection model or adjusting flagging thresholds to reduce false negatives.')
    print('In conclusion, while the system performs well for legitimate transactions, its inability to detect fraud highlights a severe gap that must be addressed for improved security.')
