from world_bank_data_interface import WbDataInterface
import gradio as gr
import pandas as pd


class Server:
    def __init__(self) -> None:
        self.wb_data_interface = WbDataInterface()
        self.page = self.build_page()
        self.cache = {}

    def run(self):
        self.page.launch()

    def build_page(self):
        """Build the page."""
        country_name_list = self.wb_data_interface.country_field_manager.get_drop_down_list()
        indicator_name_list = self.wb_data_interface.indicator_field_manager.get_drop_down_list()

        # the structure of the page
        with gr.Blocks() as page:
            gr.HTML("<h1 align=\"center\">少废话，你GDP多少？</h1>")
            with gr.Row():
                country_name = gr.Dropdown(
                    country_name_list, label="Country", value="China")
                indicator_name = gr.Dropdown(indicator_name_list,
                                             label="Indicator", value="GDP (current Local Currency Units)")
            with gr.Row():
                start_time = gr.Slider(
                    label="Start Time / Year", value=1990, minimum=1970, maximum=2023, step=1
                )
                time_interval = gr.Slider(
                    label="Time Interval / Year", value=40, minimum=5, maximum=70, step=1
                )
            plot = gr.LinePlot(show_label=False)
            button = gr.Button("Get Plot")

            inputs = [country_name,
                      indicator_name, start_time, time_interval]
            page.load(fn=self.get_plot, inputs=inputs, outputs=[plot])

            button.click(fn=self.get_plot, inputs=inputs, outputs=[plot])

            gr.Interface

        return page

    def get_plot(self, country_name, indicator_name, start_time, time_interval):
        # get data
        if (country_name, indicator_name) in self.cache:
            df = self.cache[(country_name, indicator_name)]
        else:
            df = self.wb_data_interface.get_data(country_name, indicator_name)
            self.cache[(country_name, indicator_name)] = df

        if df.shape[0] > 0:
            # filter data by time
            df = df[(df["Year"] >= start_time) &
                    (df["Year"] <= start_time + time_interval)]
        else:
            df = pd.DataFrame({"Year": [], "GDP": []})

        # generate plot
        gdp_plot = gr.LinePlot(
            value=df,
            x="Year",
            y="GDP",
            title="%s of %s from %d to %d" % (
                indicator_name, country_name, start_time, start_time + time_interval),
            width=600,
            height=350,
        )
        return gdp_plot
