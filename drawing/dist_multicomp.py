import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.width', None)

def dist_multicomp(df, filepath, cfg):
    # Define columns
    all_keys = list(df.index.get_level_values("key").unique())
    all_keys_noupdown = list(set([k.replace("Up","").replace("Down","") for k in all_keys if k != "nominal"]))
    all_columns = list(df.index.names)
    columns_nokey = [c for c in all_columns if c != "key"]
    columns_nobins = [c for c in all_columns if "bin" not in c]
    columns_nokey_nobins = [c for c in columns_nokey if "bin" not in c]

    # Remove under and overflow bins (add overflow into final bin)
    def truncate(indf):
        indf.iloc[-2] += indf.iloc[-1]
        indf = indf.iloc[1:-1]
        indf = indf.reset_index(columns_nobins, drop=True)
        return indf
    df = df.groupby(columns_nobins).apply(truncate)

    df = df.reset_index("bin0_low")
    new_bins = [-np.inf]+list(np.linspace(50., 1000., 20))+[np.inf]
    #new_bins = [-np.inf, 0., 200., 250., 300., 350., 400., 500., 600., 800., np.inf]
    df["merge_idx"] = df["bin0_low"].apply(
        lambda b: next(idx for idx, nb in enumerate(new_bins[1:]) if b<nb),
    )
    df = df.set_index("bin0_low", append=True)\
            .reorder_levels(all_columns)\
            .groupby(columns_nobins+["merge_idx"]).sum()

    df_pivot_key = df.pivot_table(
        values = 'yield',
        index = columns_nokey_nobins+["merge_idx"],
        columns = 'key',
        aggfunc = np.sum,
    )

    # MC stats.
    df_mcstat = df[df.index.get_level_values("key").isin(["nominal"])]
    df_mcstat = df_mcstat.reset_index("key", drop=True)
    df_mcstat["mcstatUp"] = df_mcstat["yield"]+np.sqrt(df_mcstat["variance"])
    df_mcstat["mcstatDown"] = df_mcstat["yield"]-np.sqrt(df_mcstat["variance"])
    df_pivot_key = pd.concat((df_pivot_key, df_mcstat[["mcstatUp", "mcstatDown"]]), axis=1)
    all_keys.extend(["mcstatUp", "mcstatDown"])
    all_keys_noupdown.append("mcstat")

    df_pivot_ratio = df_pivot_key[[k for k in all_keys if k != "nominal"]]
    df_pivot_ratio = df_pivot_ratio.div(df_pivot_key["nominal"], axis=0)

    # sum in quadrature
    df_key_perc = np.sign(df_pivot_ratio-1)*np.abs(df_pivot_ratio-1)
    for key in all_keys_noupdown:
        df_temp = df_key_perc[[key+"Up", key+"Down"]]
        df_temp["dummy"] = 0.
        df_temp["new"+key+"Up"] = df_temp.apply(np.max, axis=1)
        df_temp["new"+key+"Down"] = df_temp.apply(np.min, axis=1)
        df_key_perc[key+"Up"] = df_temp["new"+key+"Up"]
        df_key_perc[key+"Down"] = df_temp["new"+key+"Down"]

    df_key_perc_up = df_key_perc[[key+"Up" for key in all_keys_noupdown]]
    df_key_perc_up.columns = all_keys_noupdown
    df_key_perc_down = df_key_perc[[key+"Down" for key in all_keys_noupdown]]
    df_key_perc_down.columns = all_keys_noupdown

    sorted_keys = np.sqrt(((df_key_perc_up+1).prod(axis=0)-1)**2 + ((df_key_perc_down+1).prod(axis=0)-1)**2)\
            .sort_values().index.values[::-1]
    df_key_perc_up = (df_key_perc_up[sorted_keys]+1)
    df_key_perc_down = (df_key_perc_down[sorted_keys]+1)

    # Get the global bins
    bins = np.array(new_bins[1:-1])
    bin_centers = (bins[1:]+bins[:-1])/2
    bin_widths = (bins[1:]-bins[:-1])

    fig, ax = plt.subplots()
    ax.set_xlim(bins[0], bins[-1])

    # Add CMS text to top + energy + lumi
    ax.text(0, 1, r'$\mathbf{CMS}\ \mathit{Preliminary}$',
               horizontalalignment='left',
               verticalalignment='bottom',
               transform=ax.transAxes,
               fontsize='large')
    ax.text(1, 1, r'$35.9\ \mathrm{fb}^{-1}(13\ \mathrm{TeV})$',
               horizontalalignment='right',
               verticalalignment='bottom',
               transform=ax.transAxes,
               fontsize='large')

    ymax = 1.01
    ymin = 0.99
    for idx, key in reversed(list(enumerate(sorted_keys))):
        top = np.sqrt(((df_key_perc_up[sorted_keys[:idx+1]]-1)**2).sum(axis=1))+1
        bot = 1-np.sqrt(((df_key_perc_down[sorted_keys[:idx+1]]-1)**2).sum(axis=1))

        ymax = max(top.max(), ymax)
        ymin = min(bot.min(), ymin)

        ax.fill_between(
            bins, top, bot,
            step = 'post',
            color = cfg.sample_colours.get(key, 'blue'),
            label = cfg.sample_names.get(key, key),
        )
    ax.axhline(1, ls='--', color='black')

    # Legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])

    name = cfg.name
    ax.set_xlabel(cfg.axis_label.get(name, name), fontsize='large')
    ax.set_ylabel(r'Relative impact', fontsize='large')

    yrange = max(ymax-1, 1-ymin)*1.05
    ax.set_ylim((1-yrange, 1+yrange))

    # Report
    print("Creating {}.pdf".format(filepath))

    # Actually save the figure
    plt.tight_layout()
    fig.savefig(filepath+".pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)

    return df
