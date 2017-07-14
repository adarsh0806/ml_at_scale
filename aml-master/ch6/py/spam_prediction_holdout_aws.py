# ---------------------------------------------------------------------------------
#  2. Prediction on the heldout dataset
#     calculate and plot ROC-AUC
# ---------------------------------------------------------------------------------


import boto3
import json
import pandas as pd
from sklearn import metrics

# file with heldout spam dataset
filename = "/Users/adarshnair/Desktop/Machine_Learning_at_scale/aml-master/ch6/data/spam.csv"

# Initialize the Service, the Model ID and the endpoint url
client = boto3.client('machinelearning')
endpoint_url = "https://realtime.machinelearning.us-east-1.amazonaws.com"

# Replace with your model ID
model_id = "ml-pFfGptQhkPm"

# Recall which class is spam and which is ham
spam_label = {'0': 'ham', '1':'spam'}

# Load the held out dataset into a panda DataFrame
df = pd.read_csv(filename)
print df.head()
df['predicted'] = -1
df['predicted_score'] = -1

# Loop over each DataFrame rows
count = 0
for index, row in df.iterrows():
    record = { "body": row['v2'] }
    print "\n"
    print row['v2']
    print "\n"
    response = client.predict(
        MLModelId       = model_id,
        Record          = record,
        PredictEndpoint = endpoint_url
    )
    predicted_label = response['Prediction']['predictedLabel']
    predicted_score = response['Prediction']['predictedScores'][predicted_label]
    # print("[%s] %s (%0.2f):\t %s "% (spam_label[str(row['nature'])],
    #                             spam_label[predicted_label],
    #                             predicted_score,
    #                             row['sms'] )
    print spam_label[predicted_label], predicted_score

    df.loc[index, 'predicted'] = int(response['Prediction']['predictedLabel'])
    df.loc[index, 'predicted'] = int(predicted_label)
    df.loc[index, 'predicted_score'] = predicted_score
    count += 1
    if count == 30:
    	break
# Calculate ROC-AUC

fpr, tpr, threshold = metrics.roc_curve(df.nature, df.predicted_score)
roc_auc = metrics.auc(fpr, tpr)

# Plot ROC curve

import matplotlib.pyplot as plt
# %matplotlib


fig, ax = plt.subplots(1,1, figsize=(8,8))

ax.set_axis_bgcolor('white')
ax.set_title('ROC - Spam dataset')
ax.grid()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel('True Positive Rate')
ax.set_ylabel('False Positive Rate')

ax.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
ax.plot([0, 1], [0, 1],'r--')

ax.legend(loc='lower right')
ax.set_xlim(-0.05, 1.)
ax.set_ylim(0, 1.05)
plt.tight_layout()
plt.show()