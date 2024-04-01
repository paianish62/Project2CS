import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

app = tk.Tk()
app.title('Global Investment Recommender System')
app.geometry('630x800')
app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=3)
app.columnconfigure(2, weight=1)


def show_output():
    """
    abcd
    :return:
    """

    output = tk.Toplevel()
    output.title('Global Investment Recommender System')
    output.geometry('1000x750')
    output.columnconfigure(0, weight=1)
    output.columnconfigure(1, weight=6)
    output.columnconfigure(2, weight=1)
    output_title_text = "🌍  Here's where we think you should invest:"
    output_title = ttk.Label(master=output, text=output_title_text, font='Arial 23 bold', padding=(20, 30, 0, 20))
    output_title.grid(row=1, column=1, sticky='nw')

    final_data = {'India': [50, 60], 'Canada': [70, 30], 'Germany': [80, 90], 'India1': [50, 60], 'Canada1': [70, 30]}
    eco_scores = [final_data[i][0] for i in final_data]
    ethic_scores = [final_data[i][1] for i in final_data]

    plt.ioff()
    fig1, ax1 = plt.subplots(figsize=(4, 3))  # Adjust figsize as needed
    ax1.bar(final_data.keys(), eco_scores, color='#7889ED')
    ax1.set_title("Countries by Economic Score", color='white')
    ax1.set_ylabel("Economic Score", color='white')
    ax1.set_facecolor('#121828')
    fig1.set_facecolor('#121828')
    ax1.spines['bottom'].set_edgecolor('white')
    ax1.spines['left'].set_edgecolor('white')
    ax1.spines['top'].set_edgecolor('#121828')
    ax1.spines['right'].set_edgecolor('#121828')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')

    plt.ioff()
    fig2, ax2 = plt.subplots(figsize=(4, 3))  # Adjust figsize as needed
    ax2.bar(final_data.keys(), ethic_scores, color='#7889ED')
    ax2.set_title("Countries by Ethical Score", color='white')
    ax2.set_ylabel("Ethical Score", color='white')
    ax2.set_facecolor('#121828')
    fig2.set_facecolor('#121828')
    ax2.spines['bottom'].set_edgecolor('white')
    ax2.spines['left'].set_edgecolor('white')
    ax2.spines['top'].set_edgecolor('#121828')
    ax2.spines['right'].set_edgecolor('#121828')
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')

    frame = tk.Frame(output)
    frame.grid(row=2, column=1, sticky='nsew')

    canvas_eco = FigureCanvasTkAgg(fig1, frame)
    canvas_eco.draw()
    canvas_eco.get_tk_widget().grid(row=0, column=0, sticky='nsew', padx=(20, 10))

    canvas_ethic = FigureCanvasTkAgg(fig2, frame)
    canvas_ethic.draw()
    canvas_ethic.get_tk_widget().grid(row=0, column=1, sticky='nsew', padx=(10, 20))

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure([0, 1], weight=1)

    output_title_text = "Here are the countries ranked:"
    output_title = ttk.Label(master=output, text=output_title_text, font='Arial 23 bold', padding=(20, 30, 0, 20))
    output_title.grid(row=3, column=1, sticky='nw')

    # List View

    # countries = list(final_data.keys())
    # count = 4
    # rank = 1
    # for i in countries:
    #     country_title = ttk.Label(master=output, text='\t'+str(rank)+'. '+i, font='Arial 18', padding=(20, 5, 0, 20))
    #     country_title.grid(row=count, column=1, sticky='nw')
    #     count += 1
    #     rank += 1

    # Table View

    columns = ('Rank', 'Country', 'Economic Score', 'Ethical Score')
    table = ttk.Treeview(output, columns=columns, show='headings')
    for col in columns:
        table.heading(col, text=col, anchor=tk.CENTER)
        table.column(col, anchor="center")

    main_data = []
    for i in final_data:
        temp_list = [i, final_data[i][0], final_data[i][1]]
        main_data.append(temp_list)

    rank = 1
    for row in main_data:
        table.insert('', tk.END, values=[rank]+row)
        rank += 1

    table.grid(row=4, column=1, sticky='ew', padx=(20, 20), pady=(0, 100))

    output.mainloop()


def submit_func():
    """
    abcd
    """
    region = region_combo.get()
    status = dev_combo.get()
    industry = ind_combo.get()
    tree_list = [region, status, industry]
    blank = ['Region', 'Status', 'Sector']
    form_status = False
    ethic_status = False
    rank_repeat = False
    ethic_list = []

    if any(i in tree_list for i in blank):
        error_str = ''
        count = 0
        for i in tree_list:
            if i in blank:
                count += 1
                error_str += str(count)+'. '+i+'\n'
        messagebox.showwarning(
            title='Field(s) Empty',
            message='The Following Fields are empty: \n' + error_str + 'Please fill them and submit again.'
        )
    else:
        form_status = True
    digit_check = [env_combo.get().isdigit(), equi_combo.get().isdigit(), flt_combo.get().isdigit()]

    #  checking if rankings are filled or not
    if all(digit_check):
        rank = [int(env_combo.get()), int(equi_combo.get()), int(flt_combo.get())]
        rank_repeat = any(rank.count(i) > 1 for i in rank)
    else:
        messagebox.showwarning(
            title='Empty Ranking(s)',
            message='One or More Ethical Categories have not been ranked, please rank them and submit again.'
        )
    # checking if the rankings are not same
    if rank_repeat:
        rank_repeat_msg = 'One or More Ethical Categories have been ranked the same, '
        messagebox.showwarning(
            title='Ranks Repeated',
            message=rank_repeat_msg+'please rank them differently and submit again.'
        )

    if all(digit_check) and (not rank_repeat):
        ethic_status = True
        ethic_dict = {int(env_combo.get()): 'env', int(equi_combo.get()): 'equ', int(flt_combo.get()): 'lab'}
        for i in sorted(list(ethic_dict.keys())):
            ethic_list.append(ethic_dict[i])

    if ethic_status and form_status:
        print((tree_list, ethic_list))
        messagebox.showinfo(
            title='Submitted',
            message='Form successfully submitted'
        )
        show_output()


def help_func():
    """

    :return:
    """
    terms_dict = {'Economic Development Status': '', 'Sector': '', 'Developed': '', 'Emerging': '', 'Primary': '',
                  'Secondary': '', 'Tertiary': '', 'Equity': '',
                  'Fair Labour Treatment': ''}
    if help_combo.get() == 'Select':
        messagebox.showinfo(
            title='No Term Selected',
            message='Please select a term from the dropdown menu'
        )
    else:
        messagebox.showinfo(
            title=help_combo.get(),
            message=help_combo.get()+' means: '+terms_dict[help_combo.get()]
        )


# Project Title + Subtext
title_text = '🌐  Global Investment Recommender System'
title = ttk.Label(master=app, text=title_text, font='Arial 23 bold',  padding=(20, 30, 0, 0))
title.grid(row=1, column=1, sticky='nw')

subtitle1 = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \n'
subtitle_text = subtitle1 + 'labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrudexercitation ullamco.'
subtitle = ttk.Label(master=app, text=subtitle_text, font='Arial 11',  padding=(20, 8, 0, 0))
subtitle.grid(row=2, column=1, sticky='nw')

# Region
region_title_text = 'Region*'
region_title = ttk.Label(master=app, text=region_title_text, font='Arial 20 bold',  padding=(20, 20, 0, 0))
region_title.grid(row=3, column=1, sticky='nw')

region_subtitle_text = 'In which region are you considering making investments?'
region_subtitle = ttk.Label(master=app, text=region_subtitle_text, font=('Arial', 12, 'italic'),  padding=(20, 5, 0, 0))
region_subtitle.grid(row=4, column=1, sticky='nw')

region_values = ['Americas', 'Africa', 'Asia', 'Middle East', 'Europe', 'Oceana']
region_combo = ttk.Combobox(master=app, values=region_values, state='readonly')
region_combo.set('Region')
region_combo.grid(row=5, column=1, sticky='nwse', padx=(18, 100), pady=(5, 0))

# Developed or Emerging
dev_title_text = 'Economic Development Status*'
dev_title = ttk.Label(master=app, text=dev_title_text, font='Arial 20 bold',  padding=(20, 20, 0, 0))
dev_title.grid(row=6, column=1, sticky='nw')

dev_subtitle_text = 'Do you have a preference for investing in developed or emerging countries?'
dev_subtitle = ttk.Label(master=app, text=dev_subtitle_text, font=('Arial', 12, 'italic'),  padding=(20, 5, 0, 0))
dev_subtitle.grid(row=7, column=1, sticky='nw')

dev_values = ['Developed', 'Emerging']
dev_combo = ttk.Combobox(master=app, values=dev_values, state='readonly')
dev_combo.set('Status')
dev_combo.grid(row=8, column=1, sticky='nwse', padx=(18, 100), pady=(5, 0))

# Industries
ind_title_text = 'Sector*'
ind_title = ttk.Label(master=app, text=ind_title_text, font='Arial 20 bold',  padding=(20, 20, 0, 0))
ind_title.grid(row=9, column=1, sticky='nw')

ind_subtitle_text = 'Which sectors are of interest to you for potential investment?'
ind_subtitle = ttk.Label(master=app, text=ind_subtitle_text, font=('Arial', 12, 'italic'),  padding=(20, 5, 0, 0))
ind_subtitle.grid(row=10, column=1, sticky='nw')

ind_values = ['Primary', 'Secondary', 'Tertiary']
ind_combo = ttk.Combobox(master=app, values=ind_values, state='readonly')
ind_combo.set('Sector')
ind_combo.grid(row=11, column=1, sticky='nwse', padx=(18, 100), pady=(5, 0))

# Ethical Priority
ethics_title_text = 'Ethical Priority*'
ethics_title = ttk.Label(master=app, text=ethics_title_text, font='Arial 20 bold',  padding=(20, 20, 0, 0))
ethics_title.grid(row=12, column=1, sticky='nw')

ethics_subtitle1 = 'Please prioritize the following three categories\n'
ethics_subtitle_text = ethics_subtitle1 + '(1 indicating the highest priority and 3 the lowest priority.)'
ethics_subtitle = ttk.Label(master=app, text=ethics_subtitle_text, font=('Arial', 12, 'italic'),  padding=(20, 5, 0, 0))
ethics_subtitle.grid(row=13, column=1, sticky='nw')
ranks = ['1', '2', '3']

# Ethic 1: Environment
env_subtitle_text = 'Environment'
env_subtitle = ttk.Label(master=app, text=env_subtitle_text, font=('Arial', 16),  padding=(20, 10, 0, 0))
env_subtitle.grid(row=14, column=1, sticky='nw')
env_combo = ttk.Combobox(master=app, values=ranks, state='readonly', width=10)
env_combo.set('Rank')
env_combo.grid(row=14, column=1, sticky='ne', padx=(0, 100), pady=(10, 0))

# Ethic 2: Equity Score
equi_subtitle_text = 'Equity'
equi_subtitle = ttk.Label(master=app, text=equi_subtitle_text, font=('Arial', 16),  padding=(20, 15, 0, 0))
equi_subtitle.grid(row=15, column=1, sticky='nw')
equi_combo = ttk.Combobox(master=app, values=ranks, state='readonly', width=10)
equi_combo.set('Rank')
equi_combo.grid(row=15, column=1, sticky='ne', padx=(0, 100), pady=(15, 0))

# Ethic 3: Fair Labour Treatment
flt_subtitle_text = 'Fair Labour Treatment'
flt_subtitle = ttk.Label(master=app, text=flt_subtitle_text, font=('Arial', 16),  padding=(20, 15, 0, 0))
flt_subtitle.grid(row=16, column=1, sticky='nw')
flt_combo = ttk.Combobox(master=app, values=ranks, state='readonly', width=10)
flt_combo.set('Rank')
flt_combo.grid(row=16, column=1, sticky='ne', padx=(0, 100), pady=(15, 0))

# Submit
submit = ttk.Button(master=app, text='Submit', command=submit_func)
submit.grid(row=17, column=1, sticky='nswe', padx=(20, 100), pady=(20, 0))

# Help
help_text = 'Any term you do not understand? please select it and press the Help button'
help_subtitle = ttk.Label(master=app, text=help_text, font=('Arial', 13),  padding=(20, 25, 0, 0))
help_subtitle.grid(row=18, column=1, sticky='nw')
terms = ['Economic Development Status', 'Sector', 'Developed', 'Emerging', 'Primary', 'Secondary',
         'Tertiary', 'Equity', 'Fair Labour Treatment']
help_combo = ttk.Combobox(master=app, values=terms, state='readonly', width=37)
help_combo.set('Select')
help_combo.grid(row=19, column=1, sticky='nw', padx=(18, 100), pady=(5, 0))
help_btn = ttk.Button(master=app, text='Help', command=help_func)
help_btn.grid(row=19, column=1, sticky='ne', padx=(20, 100), pady=(5, 0))

app.mainloop()
