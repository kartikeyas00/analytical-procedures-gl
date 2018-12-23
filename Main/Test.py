# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 00:39:40 2018

@author: karti
"""

from Classes.class_je_tests import journal_entries_testing

if __name__ == "__main__":
    je_test=journal_entries_testing("General Ledger.xlsx")
    je_test.load_file()
    je_test.clean_file()
    print(je_test.pivot_table())
    print(je_test.check_for_unbalance_journal_entries())
    print(je_test.check_journal_entries_on_weekend())
    print(je_test.check_high_dollar_journal_entries())
    print(je_test.check_all_entries_with_specific_account())
    print(je_test.find_round_dollar_journal_entries())
    print(je_test.obtain_sample_journal_entries())
    print(je_test.find_specific_general_entries_monthordays())
    print(je_test.find_gaps_journal_entries_sequence())
    print(je_test.scatter_graph_journal_entries_credits_and_debits())
    