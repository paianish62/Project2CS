"""
This file contains the frontend implementation of our program to create a user-friendly and aesthetically appealing
user-interface. Leveraging Tkinter for the graphical user interface, it guides users through a series of investment
criteria, including region, economic development status, sector of interest, and ethical priorities.
Utilizing matplotlib for data visualization, the application presents a comparative analysis of countries
based on economic and ethical scores. The goal is to provide users with a comprehensive and accessible tool
for making informed investment decisions grounded in both economic performance and ethical considerations.

Copyright © 2023 Global Investment Recommender System (GIRS). All rights reserved.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import treetry
import load_data


def show_output(treelist: list, ethiclist: list) -> None:
    """
    This function is designed to display the output after analyzing the user's inputs.
    It presents visuals for 'Countries by Economic Growth' and 'Countries by Ethical Score,'
    as well as a table listing all the recommended countries ranked according to their average
    score.
    """

    output = tk.Toplevel()
    output.title('Global Investment Recommender System')
    output.geometry('1250x750')
    output.columnconfigure(0, weight=1)
    output.columnconfigure(1, weight=6)
    output.columnconfigure(2, weight=1)
    output_title_text = "🌍  Here's where we think you should invest:"
    output_title = ttk.Label(master=output, text=output_title_text, font='Arial 23 bold', padding=(20, 30, 0, 20))
    output_title.grid(row=1, column=1, sticky='nw')
    countries_of_interest = {'United States': 'US', 'Canada': 'CA', 'Brazil': 'BR', 'Mexico': 'MX', 'Argentina': 'AR',
                             'Uruguay': 'UY', 'South Africa': 'ZA', 'Mauritius': 'MU', 'Botswana': 'BW',
                             'Australia': 'AU', 'New Zealand': 'NZ', 'Singapore': 'SG', 'China': 'CN', 'India': 'IN',
                             'Japan': 'JP', 'Russia': 'RU', 'South Korea': 'KR', 'Indonesia': 'ID',
                             'Saudi Arabia': 'SA', 'Qatar': 'QA', 'Turkey': 'TR', 'Oman': 'OM', 'Germany': 'DE',
                             'United Kingdom': 'GB', 'France': 'FR', 'Italy': 'IT', 'Spain': 'ES',
                             'Netherlands': 'NL', 'Switzerland': 'CH', 'Poland': 'PL'}

    gdp_info = load_data.load_stored_pickle('gdp.pickle')
    cpi_info = load_data.load_stored_pickle('cpi.pickle')
    sectors_info = load_data.extract_sector_gdp_percentage(load_data.sector_info_file, load_data.countries_of_interest)
    interest = load_data.extract_interest_time_series(load_data.interest_info_file,
                                                      load_data.countries_of_interest)
    region_development = load_data.extract_region_info(load_data.region_info_file, load_data.countries_of_interest)
    sdg_info = load_data.extract_sdg_info(load_data.sdg_info_file, load_data.countries_of_interest)

    # Getting the final data and sorting and ranking it.
    countries_query = treetry.main_func(region_development, sectors_info, gdp_info, sdg_info, ethiclist, treelist,
                                        cpi_info, interest)
    final_data = countries_query[0]
    if countries_query[1] == 1:
        rec_title_text = ("Sorry, we did not find countries that matched your exact specifications. However, "
                          "we found some that were close.")
        rec_title = ttk.Label(master=output, text=rec_title_text, font='Arial 18', padding=(20, 10, 0, 20))
        rec_title.grid(row=2, column=1, sticky='nw')
    elif countries_query[1] == 2:
        rec_title_text = ("Sorry, your search did not return any specific or similar matches, but here is a list of "
                          "the top 5 countries to invest in ranked.")
        rec_title = ttk.Label(master=output, text=rec_title_text, font='Arial 18', padding=(20, 10, 0, 20))
        rec_title.grid(row=2, column=1, sticky='nw')

    eco_scores = [round(final_data[p][0], 2) for p in final_data]
    ethic_scores = [round(final_data[j][1], 2) for j in final_data]
    avg_scores = {}
    for i in final_data:
        avg_score = round(sum(final_data[i]) / 2, 2)
        if avg_score not in avg_scores:
            avg_scores[avg_score] = [i]
        else:
            avg_scores[avg_score].append(i)
    sorted_avg_scores = sorted(list(avg_scores.keys()), reverse=True)
    ranked_countries = []
    for i in sorted_avg_scores:
        ranked_countries.extend(sorted(avg_scores[i], reverse=True))

    # Plotting Graphs
    plt.ioff()
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    country_codes = [countries_of_interest[k] for k in final_data]
    ax1.bar(country_codes, eco_scores, color='#7889ED')
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
    fig2, ax2 = plt.subplots(figsize=(4, 3))
    ax2.bar(country_codes, ethic_scores, color='#F06449')
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
    frame.grid(row=3, column=1, sticky='nsew')

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
    output_title.grid(row=4, column=1, sticky='nw')

    # Table View

    columns = ('Rank', 'Country', 'Country Code', 'Average Score', 'Economic Score', 'Ethical Score')
    table = ttk.Treeview(output, columns=columns, show='headings')
    for col in columns:
        table.heading(col, text=col, anchor=tk.CENTER)
        table.column(col, anchor="center")

    main_data = []
    rank = 1
    for i in ranked_countries:
        eco_score = round(final_data[i][0], 2)
        avg = round(sum(final_data[i]) / 2, 2)
        ethic_score = round(final_data[i][1], 2)
        temp_list = [rank, i, countries_of_interest[i], avg, eco_score, ethic_score]
        main_data.append(temp_list)
        rank += 1

    for row in main_data:
        table.insert('', tk.END, values=row)

    table.grid(row=5, column=1, sticky='ew', padx=(20, 20), pady=(0, 100))

    output.mainloop()


def run() -> None:
    """
    This function displays the input screen, presented as a form where users can fill in the
    necessary input fields and submit them for processing by our backend functionality.
    """
    def submit_func() -> None:
        """
        This function is called whenever the user presses the submit button.
        It handles cases where the user has left any input fields empty or has assigned the
        same ranking to any of the ethical categories. If none of these issues are present,
        it submits the user's inputs for processing and analysis and then displays the
        output screen.
        """
        sector = ind_combo.get().lower()
        tree_list = [region_combo.get().lower(), dev_combo.get().lower(), inv_combo.get().lower(), sector]
        blank = ['region', 'status', 'sector', 'term']
        form_status = False
        ethic_status = False
        rank_repeat = False
        ethic_list = []

        if any(n.lower() in tree_list for n in blank):
            error_str = ''
            count = 0
            for i in tree_list:
                if i in blank:
                    count += 1
                    error_str += str(count) + '. ' + i.capitalize() + '\n'
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
            rank_repeat = any(rank.count(m) > 1 for m in rank)
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
                message=rank_repeat_msg + 'please rank them differently and submit again.'
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
            show_output(tree_list, ethic_list)

    def help_func() -> None:
        """
        This function is called whenever the user presses the help button.
        It checks which term the user has selected and displays its meaning or
        definition using a messagebox
        """
        eds = "A classification indicating a country's level of economic growth and stability."
        sec = "A segment of the economy, often categorized into primary (resource extraction), \
               secondary (manufacturing), and tertiary (services) sectors, reflecting different types \
               of economic activities."
        dev = "Refers to countries with high levels of industrialization, a high standard \
                of living, and advanced technological infrastructure."
        em = "Describes nations that are in the process of rapid industrialization and have growing economies, often \
              experiencing fast-paced economic growth and development."
        prim = "The sector of the economy focused on the extraction and collection of \
                natural resources, such as agriculture, mining, and forestry."
        second = "This sector involves processing, manufacturing, and construction, transforming \
                raw materials into finished goods and buildings."
        tert = "The sector that provides services instead of goods, including healthcare, education, retail, and \
                financial services."
        equit = "Fairness and equality in rights, opportunities, and treatment between genders, aiming to eliminate \
                discrimination and ensure equal access for all."
        labour = "Ensuring workers are treated ethically and legally, including fair wages, safe \
                working conditions, and respect for their rights."
        invt = "The period over which money is invested."
        lt = "Investments held for several years or more, typically aiming for larger gains over time."
        st = "Investments held for a short period, usually less than a year, focusing on quick gains."
        terms_dict = {'Economic Development Status': eds, 'Sector': sec, 'Developed': dev, 'Emerging': em,
                      'Primary': prim, 'Secondary': second, 'Tertiary': tert, 'Equity': equit,
                      'Fair Labour Treatment': labour, 'Investment Terms': invt, 'Long Run': lt, 'Short Run': st}

        if help_combo.get() == 'Select':
            messagebox.showinfo(
                title='No Term Selected',
                message='Please select a term from the dropdown menu'
            )
        else:
            messagebox.showinfo(
                title=help_combo.get(),
                message=help_combo.get() + ': ' + terms_dict[help_combo.get()]
            )

    app = tk.Tk()
    app.title('Global Investment Recommender System')
    app.geometry('630x1000')
    app.columnconfigure(0, weight=1)
    app.columnconfigure(1, weight=3)
    app.columnconfigure(2, weight=1)

    # Project Title + Subtext
    title_text = '🌐  Global Investment Recommender System'
    title = ttk.Label(master=app, text=title_text, font='Arial 23 bold', padding=(20, 20, 0, 0))
    title.grid(row=1, column=1, sticky='nw')

    subtitle1 = 'Empower your investments. Leverage economic data and ethical insights to \nsmartly navigate'
    subtitle_text = subtitle1 + 'global markets and uncover tailored opportunities.'
    subtitle = ttk.Label(master=app, text=subtitle_text, font='Arial 11', padding=(20, 8, 0, 0))
    subtitle.grid(row=2, column=1, sticky='nw')

    # Region
    region_title_text = 'Region*'
    region_title = ttk.Label(master=app, text=region_title_text, font='Arial 20 bold', padding=(20, 15, 0, 0))
    region_title.grid(row=3, column=1, sticky='nw')

    region_subtitle_text = 'In which region are you considering making investments?'
    padd = (20, 5, 0, 0)
    region_subtitle = ttk.Label(master=app, text=region_subtitle_text, font=('Arial', 12, 'italic'), padding=padd)
    region_subtitle.grid(row=4, column=1, sticky='nw')

    region_values = ['Americas', 'Africa', 'Asia', 'Europe', 'Oceania']
    region_combo = ttk.Combobox(master=app, values=region_values, state='readonly')
    region_combo.set('Region')
    region_combo.grid(row=5, column=1, sticky='nwse', padx=(18, 100), pady=(5, 0))

    # Developed or Emerging
    dev_title_text = 'Economic Development Status*'
    dev_title = ttk.Label(master=app, text=dev_title_text, font='Arial 20 bold', padding=(20, 15, 0, 0))
    dev_title.grid(row=6, column=1, sticky='nw')

    dev_subtitle_text = 'Do you have a preference for investing in developed or emerging countries?'
    dev_subtitle = ttk.Label(master=app, text=dev_subtitle_text, font=('Arial', 12, 'italic'), padding=(20, 5, 0, 0))
    dev_subtitle.grid(row=7, column=1, sticky='nw')

    dev_values = ['Developed', 'Emerging']
    dev_combo = ttk.Combobox(master=app, values=dev_values, state='readonly')
    dev_combo.set('Status')
    dev_combo.grid(row=8, column=1, sticky='nwse', padx=(18, 100), pady=(5, 0))

    # Investment Terms

    inv_title_text = 'Investment Terms*'
    inv_title = ttk.Label(master=app, text=inv_title_text, font='Arial 20 bold', padding=(20, 15, 0, 0))
    inv_title.grid(row=9, column=1, sticky='nw')

    inv_subtitle_text = "What's your investment horizon: short-term or long-term?"
    inv_subtitle = ttk.Label(master=app, text=inv_subtitle_text, font=('Arial', 12, 'italic'), padding=(20, 5, 0, 0))
    inv_subtitle.grid(row=10, column=1, sticky='nw')

    inv_values = ['Long Run', 'Short Run']
    inv_combo = ttk.Combobox(master=app, values=inv_values, state='readonly')
    inv_combo.set('Term')
    inv_combo.grid(row=11, column=1, sticky='nwse', padx=(18, 100), pady=(5, 0))

    # Industries
    ind_title_text = 'Sector*'
    ind_title = ttk.Label(master=app, text=ind_title_text, font='Arial 20 bold', padding=(20, 15, 0, 0))
    ind_title.grid(row=12, column=1, sticky='nw')

    ind_subtitle_text = 'Which sectors are of interest to you for potential investment?'
    ind_subtitle = ttk.Label(master=app, text=ind_subtitle_text, font=('Arial', 12, 'italic'), padding=(20, 5, 0, 0))
    ind_subtitle.grid(row=13, column=1, sticky='nw')

    ind_values = ['Primary', 'Secondary', 'Tertiary']
    ind_combo = ttk.Combobox(master=app, values=ind_values, state='readonly')
    ind_combo.set('Sector')
    ind_combo.grid(row=14, column=1, sticky='nwse', padx=(18, 100), pady=(5, 0))

    # Ethical Priority
    ethics_title_text = 'Ethical Priority*'
    ethics_title = ttk.Label(master=app, text=ethics_title_text, font='Arial 20 bold', padding=(20, 15, 0, 0))
    ethics_title.grid(row=15, column=1, sticky='nw')

    ethics_subtitle1 = 'Please prioritize the following three categories\n'
    ethics_subtitle_text = ethics_subtitle1 + '(1 indicating the highest priority and 3 the lowest priority.)'
    padd_e = (20, 5, 0, 0)
    ethics_subtitle = ttk.Label(master=app, text=ethics_subtitle_text, font=('Arial', 12, 'italic'), padding=padd_e)
    ethics_subtitle.grid(row=16, column=1, sticky='nw')
    ranks = ['1', '2', '3']

    # Ethic 1: Environment
    env_subtitle_text = 'Environment'
    env_subtitle = ttk.Label(master=app, text=env_subtitle_text, font=('Arial', 16), padding=(20, 10, 0, 0))
    env_subtitle.grid(row=17, column=1, sticky='nw')
    env_combo = ttk.Combobox(master=app, values=ranks, state='readonly', width=10)
    env_combo.set('Rank')
    env_combo.grid(row=17, column=1, sticky='ne', padx=(0, 100), pady=(10, 0))

    # Ethic 2: Equity Score
    equi_subtitle_text = 'Equity'
    equi_subtitle = ttk.Label(master=app, text=equi_subtitle_text, font=('Arial', 16), padding=(20, 15, 0, 0))
    equi_subtitle.grid(row=18, column=1, sticky='nw')
    equi_combo = ttk.Combobox(master=app, values=ranks, state='readonly', width=10)
    equi_combo.set('Rank')
    equi_combo.grid(row=18, column=1, sticky='ne', padx=(0, 100), pady=(15, 0))

    # Ethic 3: Fair Labour Treatment
    flt_subtitle_text = 'Fair Labour Treatment'
    flt_subtitle = ttk.Label(master=app, text=flt_subtitle_text, font=('Arial', 16), padding=(20, 15, 0, 0))
    flt_subtitle.grid(row=19, column=1, sticky='nw')
    flt_combo = ttk.Combobox(master=app, values=ranks, state='readonly', width=10)
    flt_combo.set('Rank')
    flt_combo.grid(row=19, column=1, sticky='ne', padx=(0, 100), pady=(15, 0))

    # Submit
    submit = ttk.Button(master=app, text='Submit', command=submit_func)
    submit.grid(row=20, column=1, sticky='nswe', padx=(20, 100), pady=(15, 0))

    # Help
    help_text = 'Any term you do not understand? please select it and press the Help button'
    help_subtitle = ttk.Label(master=app, text=help_text, font=('Arial', 13), padding=(20, 20, 0, 0))
    help_subtitle.grid(row=21, column=1, sticky='nw')
    terms = ['Economic Development Status', 'Investment Terms', 'Sector', 'Developed', 'Emerging', 'Primary',
             'Secondary', 'Tertiary', 'Long Run', 'Short Run', 'Equity', 'Fair Labour Treatment']
    help_combo = ttk.Combobox(master=app, values=terms, state='readonly', width=37)
    help_combo.set('Select')
    help_combo.grid(row=22, column=1, sticky='nw', padx=(18, 100), pady=(5, 0))
    help_btn = ttk.Button(master=app, text='Help', command=help_func)
    help_btn.grid(row=22, column=1, sticky='ne', padx=(20, 100), pady=(5, 0))

    app.mainloop()


if __name__ == "__main__":
    run()
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'matplotlib.backends.backend_tkagg', 'matplotlib.pyplot', 'treetry', 'load_data'],
        'allowed-io': [],
        'max-line-length': 120
    })
