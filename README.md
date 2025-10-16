# mRNA Stability Project

## Step 1: Gather, clean, and combine the data

We will need two types of data:
 - mRNA half-lives from human gene transcripts
    - I found a dataset from [this paper](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-022-02811-x#availability-of-data-and-materials) that came out in 2022!
 - Reference human cDNA / transcript FASTA file to extract UTRs

## Step 2: Embed UTRs using DNABERT-2

In order to plot or predict anything using sequence data, we have to convert the sequence into something the computer will understand: numbers. DNABERT-2 is a foundational transformer that is trained to extract meaningful motifs and characteristics out of a DNA sequence and embed them in a way for the computer to retain the significance of the sequence when transforming it into numbers. It has been trained to learn motifs significant in other areas of interest like epigenetics and transcription factor binding.

Here is a link to the PDF if you want to give it a read: https://arxiv.org/pdf/2306.15006

## Step 3: Plot UTR embeddings on a UMAP to see if they cluster by length of half-life

Plotting the embeddings on a UMAP can help us visualize in a lower-dimensional space if there are meaningful clusters or any predictive power to our data. Based on what the UMAP looks like, we will be able to make more informed decisions about which ML models to use.

## Step 4: Train different regression models on UTR embeddings

Based on the project, I think a regression model would be more fitting, but if there isn't as much predictive power as we want to see, we could also trying binning the half-lives and using a classifier. We can make an informed decision on which ML model to use once we have the UMAP results. Sci-kit learn has a lot of regressors that are easy to implement, so we will use sci-kit learn.

## Step 5: Evaluate half-life predictions of unseen transcripts

If we use a regressor, we can use L2 as our loss function. Possible plots showing model performance include:
- predicted vs actual plot
- histogram or Q-Q plot of residuals
- feature importance plot
- learning curve

Metrics to include:
- MSE
- Adjusted R squared


Happy to be here!