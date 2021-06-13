import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title("Stock Price test")
try:
    st.sidebar.write("""
    # Stockprice
    以下のオプションから表示日数を指定できます。
    """)

    st.sidebar.write("""
    ## 表示日数選択
    """)

    days = st.sidebar.slider('日数', 1, 50, 20)

    st.write(f"""
    ### 過去**{days}**日間の株価
    """)

    tickers = {
        'apple': 'AAPL',
        'facebook': 'FB',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN'
    }
    @st.cache
    def get_data(days, tickers):
        df = pd.DataFrame()
        for company in tickers.keys():
            tkr = yf.Ticker(tickers[company])
            hist = tkr.history(period = f'{days}d')
            hist.index = hist.index.strftime('%d %B %Y')
            hist = hist[['Close']]
            hist.columns = [company]
            hist = hist.T
            hist.index.name = 'Name'
            df = pd.concat([df, hist])
        return df

    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください',
        0.0, 4000.0, (0.0,3500.0)
    )

    df = get_data(days,tickers)

    companies = st.multiselect(
        '会社名を選択',
        list(df.index),
        ['google','amazon','facebook','apple']
    )

    if not companies:
        st.error('1社以上選択してください')
    else:
        data = df.loc[companies].sort_index()
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns = {'value': 'Stock Prices(USD)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x='Date:T',
                y=alt.Y('Stock Prices(USD):Q', stack=None, scale=alt.Scale(domain=[ymin,ymax])),
                color='Name:N'
                )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "Error"
    )
