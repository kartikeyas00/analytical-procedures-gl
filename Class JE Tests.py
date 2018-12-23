# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 17:35:07 2018

@author: karti
"""

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from collections import deque

class journal_entries_testing:
    def __init__(self, file_path):
        self.file_path=file_path
        
    def load_file(self):
        """
        this function loads the original file from the specified path.
        """
        self.gl = pd.read_excel(r"%s"%self.file_path)
        #return self.gl
    
    def clean_file(self):
        """
        This function cleans up the original General Ledger File. Also it 
        creates a new column Net which is the difference of the credit and 
        debit columns. It drops unnecessary rows and columns.
        """
        self.gl = self.gl.dropna(axis=1, how='all')
        acct = self.gl.index.get_level_values(0).tolist()
        for i in acct:
            if str(i).strip().startswith('Total'):
                acct[acct.index(i)]= np.nan
        for i in acct:
            if pd.isnull(i):
                acct[acct.index(i)]= acct[acct.index(i)-1]
        self.gl = self.gl.reset_index(drop=True)
        self.gl['Acct'] = pd.Series(acct)
        date=list(self.gl["Date"])
        for i in date:
            if type(i)==datetime.datetime:
                date[date.index(i)]= i.strftime('%m/%d/%Y')
        self.gl["Date"]=date
        self.gl[['Debit', 'Credit']] = self.gl[['Debit', 'Credit']].fillna(0)
        self.gl = self.gl[pd.notnull(self.gl.Date)]
        #self.gl["Date"]=self.gl["Date"].astype(str)
        self.gl=self.gl[~self.gl.Date.str.contains("Beginning Balance")]
        self.gl['Net']=self.gl['Debit']-self.gl['Credit']
        columns = ['Acct', 'Date','Transaction Type','Num', 'Name', 'Memo/Description',
                       'Split', 'Debit','Credit','Net','Balance']
        self.gl = self.gl[columns]
        self.gl = self.gl.reset_index(drop=True)
        self.gl = self.gl.fillna('NA')
        self.gl['Date'] =  pd.to_datetime(self.gl['Date'], format='%m/%d/%Y')
        self.gl['Date'] = self.gl['Date'].apply(pd.datetime.date)
        
        
    def pivot_table(self):
        """
        This function creates a pivot table by summing up the account activies
        together.
        """
        self.pivot = self.gl.pivot_table(values=['Debit', 'Credit', 'Net'], index='Acct', aggfunc='sum', margins=True)
        accts = list(self.gl.Acct.unique())
        accts.append('All')
        self.pivot.loc[accts]
        self.pivot["Net"]= self.pivot["Net"].round()
        return self.pivot
        
    
    def file(self):
        """
        this function returns the General Ledger file 
        """
        return self.gl

    def check_for_unbalance_journal_entries(self):
         """
         This function checks if there is any unbalanced journal entries in the
         General Ledger and if there is then it prints all the unbalanced journal
         entries.
         """
         account_number = np.unique(np.array(self.gl[self.gl["Transaction Type"]== "Journal Entry"].Num))
         #account_number.remove('NA')
         journal_entries=deque() #deque append performance is consistent in comparison to list because it never reallocs and never moves data.
         for i in account_number:
             data_frame_temp=self.gl[self.gl.Num==i]
             Credit_total=data_frame_temp["Credit"].sum()
             Debit_total=data_frame_temp["Debit"].sum()
             if round(Credit_total) != round(Debit_total):
                 journal_entries.append(i)
         df = pd.DataFrame(np.array(journal_entries)) #putting the results in the csv file
         if df.empty:
             print('All JOURNAL ENTRIES ARE BALANCED')
         else:    
             return df
             
    def check_journal_entries_on_weekend(self):
        """
         This function checks if there is any journal entries made in the
         weekend and if there is then it prints all the unbalanced journal
         entries.
         """
        start = pd.datetime(2018, 1, 1).date()
        end = pd.datetime(2018, 12, 31).date()
        delta = datetime.timedelta(days=1)
        d = start
        #diff = 0
        weekend = set([5, 6])
        c=[]
        while d <= end:
            if d.weekday() in weekend:
                data_frame_temp=self.gl[self.gl.Date==d]
                c.append(data_frame_temp)        
            d += delta
        df_=pd.concat(c, ignore_index=True)
        if df_.empty:
             print('NO JOURNAL ENTRIES ARE MADE ON WEEKEND')
        else:    
             return df_
             
    def greater(self,a,b):
        if a>b:
            return a
        else: 
            return b
        
    def check_high_dollar_journal_entries(self): 
        """
        This function takes in a value as an input and returns a dataframe with
        journal entries greater than the value.
        """
        val=int(input("Write the Amount you want to see for High Dollar General Entry --->"))
        account_number = np.unique(np.array(self.gl[self.gl["Transaction Type"]== "Journal Entry"].Num))
        #account_number.remove('NA')
        journal_entries={}
        for i in account_number:
            data_frame_temp=self.gl[self.gl.Num==i]
            Credit_total=data_frame_temp["Credit"].sum()
            Debit_total=data_frame_temp["Debit"].sum()
            if round(Credit_total) > val or round(Debit_total) > val: #Only in case when the journal entries are not balancing
                journal_entries[i]= self.greater(Credit_total,Debit_total)
        df=pd.DataFrame({"Journal Entries": list(journal_entries.keys()), "value": list(journal_entries.values())}) 
        if df.empty:
             print('NO JOURNAL ENTRIES ARE GREATER THAN THE VALUE ASSIGNED')
        else:    
             return df
    
    def check_all_entries_with_specific_account(self): 
        """
        This function takes in a value as an input and returns a dataframe with
        journal entries with than value.
        """
        val=input("Please write the account name here --->")
        account_number = np.unique(np.array(self.gl[self.gl["Transaction Type"]== "Journal Entry"].Num))
        #account_number.remove('NA')
        c=[]
        for i in account_number:
            data_frame_temp=self.gl[self.gl.Num==i]
            if val in list(data_frame_temp["Acct"]):
                c.append(data_frame_temp)
        df_=pd.concat(c, ignore_index=True)
        if df_.empty:
             print('NO JOURNAL ENTRIES WITH THAT SPECIFIC AMOUNT')
        else:    
             return df_ 
         
    def find_round_dollar_journal_entries(self):
        """
        This function finds all the journal entries which are exact multiple
        of $1000 and returns a dataframe with all the round dollar journal 
        entries.
        """
        account_number = np.unique(np.array(self.gl[self.gl["Transaction Type"]== "Journal Entry"].Num))
        #account_number.remove('NA')
        f=[]
        for i in account_number:
            data_frame_temp=self.gl[self.gl.Num==i]
            c=list(data_frame_temp["Credit"])
            c=list(filter(lambda a: a != 0, c))
            d=list((data_frame_temp["Debit"]))
            d=list(filter(lambda a: a != 0, d))
            cnd=zip(c,d)
            for j,k in cnd:
                if (j%1000==0 or k%1000==0):
                    f.append(data_frame_temp)
                    break
        if not f:
            print('NO ROUND JOURNAL ENTRIES IN THE GENERAL LEDGER')
        else:
            df_=pd.concat(f, ignore_index=True)
            return df_  

    def obtain_sample_journal_entries(self): 
        """
        This function takes in a value as an input and returns a dataframe with
        requested number(value) of sample journal entries
        """
        val=int(input("How many journal entries do you want to see in the sample --->"))
        account_number = np.unique(np.array(self.gl[self.gl["Transaction Type"]== "Journal Entry"].Num))
        #account_number.remove('NA')
        account_number=np.random.choice(account_number,val)
        f=[]
        for i in account_number:
            data_frame_temp=self.gl[self.gl.Num==i]
            f.append(data_frame_temp)
        if not f:
            print('ZERO ENTRIES ARE REQUESTED')
        else:
            df_=pd.concat(f, ignore_index=True)
            return df_ 

    def find_specific_general_entries_monthordays(self): 
        """
        This function takes in month or journal entry number and returns 
        the dataframe with the journal entries.
        """
        start=input("Please choose from Month or Journal Entry Number. For Month type 1 and For Journal Entry Number type 2 --->")
        if start == "1":
            montha=input("Type Month --->")
            month_number = datetime.datetime.strptime(montha, '%b').month
            df = self.gl[pd.to_datetime(self.gl['Date']).dt.month == month_number]
            df=df[df["Transaction Type"]=="Journal Entry"].sort_values("Num")
            if df.empty:
                print("No Journal entries in the chosen month")
            else:                
                return df
        if start == "2":
            journal_number=input("Type your number --->")
            data_frame_temp=self.gl[self.gl.Num==journal_number]
            if data_frame_temp.empty:
                print("Journal Entry Number doesn't exist")
            else:                
                return data_frame_temp      
        else:
            print("Wrong INPUT")
            
    def find_journal_entries_with_specific_accounts(self):
        """
        """
        account_val=input("Please put the account name --->")
        temp_gl=self.gl[self.gl["Acct"]==account_val]
        temp_gl_je=temp_gl[temp_gl["Transaction Type"]=="Journal Entry"]
        account_number = np.unique(np.array(temp_gl_je.Num))
        f=[]
        for i in account_number:
            data_frame_temp=self.gl[self.gl.Num==i]
            f.append(data_frame_temp)
        if not f:
            print('No Journal Entries in the account specified.')
        else:
            df_=pd.concat(f, ignore_index=True)
            return df_  
                        
    def find_gaps_journal_entries_sequence(self):
        """
        This function finds gap in the sequence of the journal entry and returns
        the list of all the numbers which are not in the sequence.
        """
        account_number = np.unique(np.array(self.gl[self.gl["Transaction Type"]== "Journal Entry"].Num))
        gap_account_number=deque()
        for i in range(account_number[0],account_number[-1]):
            if i not in account_number:
                gap_account_number.append(i)
        if not gap_account_number:
            print("There is no GAP in the Journal Entries sequence")
        else:
            return list(gap_account_number)
                 
    def scatter_graph_journal_entries_credits_and_debits(self): 
        """
        This function return the scatter graph of debits and credits from the 
        journal entries.
        """
        account_number = list(set(list(self.gl.Num)))
        account_number.remove('NA')
        credit=[]
        debit=[]
        for i in account_number:
            data_frame_temp=self.gl[self.gl.Num==i]
            Credit_total=data_frame_temp["Credit"].sum()
            Debit_total=data_frame_temp["Debit"].sum()
            credit.append(Credit_total)
            debit.append(Debit_total)
        number_of_transaction=list(range(1,(len(credit)+1)))
        #return [len(credit),len(debit),len(number_of_transaction)]    
        plt.title("Scatter Plot of dollar value of Debits against Number of Transactions")
        plt.xlabel("Chronological Order of Transaction")
        plt.ylabel("Dollar Value ($)")
        creds=plt.scatter(number_of_transaction,credit,label="Credit")
        debits=plt.scatter(number_of_transaction,debit,label="Debit")
        plt.legend((creds,debits),
               ('Credit','Debit'),
               scatterpoints=1,
               loc='best',
               ncol=3,
               fontsize=14)  
        plt.savefig('scatter_plot_debits.png',dpi=600)
        
