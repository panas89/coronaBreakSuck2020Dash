# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from assets.extraction import RelationExtractor
from assets.input_data import *

# corpus_text = ''
# for abstract in df.loc[:2,'abstract'].values:
#     corpus_text += abstract
corpus_text = "Transmissible gastroenteritis virus (TGEV), porcine epidemic diarrhoea virus (PEDV), and porcine deltacoronavirus (PDCoV) are enteropathogenic coronaviruses (CoVs) of swine. TGEV appearance in 1946 preceded identification of PEDV (1971) and PDCoV (2009) that are considered as emerging CoVs. A spike deletion mutant of TGEV associated with respiratory tract infection in piglets appeared in 1984 in pigs in Belgium and was designated porcine respiratory coronavirus (PRCV). PRCV is considered non-pathogenic because the infection is very mild or subclinical. Since PRCV emergence and rapid spread, most pigs have become immune to both PRCV and TGEV, which has significantly reduced the clinical and economic importance of TGEV. In contrast, PDCoV and PEDV are currently expanding their geographic distribution, and there are reports on the circulation of TGEV-PEDV recombinants that cause a disease clinically indistinguishable from that associated with the parent viruses. TGEV, PEDV and PDCoV cause acute gastroenteritis in pigs (most severe in neonatal piglets) and matches in their clinical signs and pathogenesis. Necrosis of the infected intestinal epithelial cells causes villous atrophy and malabsorptive diarrhoea. Profuse diarrhoea frequently combined with vomiting results in dehydration, which can lead to the death of piglets. Strong immune responses following natural infection protect against subsequent homologous challenge; however, these viruses display no cross-protection. Adoption of advance biosecurity measures and effective vaccines control and prevent the occurrence of diseases due to these porcine-associated CoVs. Recombination and reversion to virulence are the risks associated with generally highly effective attenuated vaccines necessitating further research on alternative vaccines to ensure their safe application in the field."

# initiate the extractor
rextractor = RelationExtractor("assets/Davids_interest_meshed.yaml")
# extract


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        dcc.Input(id="input-1", type="text", value="electroconvulsive", debounce=True),
        dcc.Input(id="input-2", type="text", value="COVID-19", debounce=True),
        html.Div(id="number-output"),
    ]
)


@app.callback(
    Output("number-output", "children"),
    [Input("input-1", "value"), Input("input-2", "value")],
)
def update_output(input1, input2):
    relation = rextractor.extract(corpus_text, input1, input2)
    if relation == None:
        return u"{} and {} have no association".format(input1, input2)
    else:
        return u"{} and {} {} association with coeff. {}".format(
            input1, input2, relation[2][0], str(relation[2][1])
        )


if __name__ == "__main__":
    app.run_server(debug=True)