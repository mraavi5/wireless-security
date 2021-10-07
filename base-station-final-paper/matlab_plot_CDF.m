global show_windows marker_size line_width line_width_dotted font_size font_size_legend;
show_windows = 'on';
marker_size = 15;
line_width = 5;
line_width_dotted = 3;
font_size = 24;
font_size_legend = 19;
legend_pos = 'SouthEast';

plotnum = 4
base_station_core = 2

if base_station_core == 1
    data_cellular = readmatrix('postprocessed_before_base_station_att-5g-100samples.csv', 'Delimiter', ',', 'LineEnding', '\n');
    data_univ_wifi = readmatrix('postprocessed_before_base_station_uccs-tracert-10samples.csv', 'Delimiter', ',', 'LineEnding', '\n');
    data_home_wifi = readmatrix('postprocessed_before_base_station_apt-tracert-100samples.csv', 'Delimiter', ',', 'LineEnding', '\n');
else
    data_cellular = readmatrix('postprocessed_before_core_network_att-5g-100samples.csv', 'Delimiter', ',', 'LineEnding', '\n');
    data_univ_wifi = readmatrix('postprocessed_before_core_network_uccs-tracert-10samples.csv', 'Delimiter', ',', 'LineEnding', '\n');
    data_home_wifi = readmatrix('postprocessed_before_core_network_apt-tracert-100samples.csv', 'Delimiter', ',', 'LineEnding', '\n');
end

fig = figure();
fig.Position = [100 100 580+100 580+100]


if plotnum == 1
    y = data_cellular(:, 3)
    histogram(y, 'Normalization', 'pdf')
    %c = cdfplot(y);
    title('');
    xlabel('Latency of Core Network (ms)')
elseif plotnum == 2
    %piedata = [247/1000 753/1000];
    piedata = [247, 753];
    c = pie(piedata, '%.1f%%')
    title('');
    title('Number of Hops to 5G Core')
    legend('4 hops', '5 hops');
elseif plotnum == 3
    piedata = [1000];
    c = pie(piedata, '%.1f%%')
    title('');
    title('Number of Hops to 5G Core')
    legend('4 hops')
elseif plotnum == 4
    % Combined all three CDFs
    y_c = data_cellular(:, 3)
    y_u = data_univ_wifi(:, 3)
    y_h = data_home_wifi(:, 3)
    hold on;
    c = cdfplot(y_c);
    c2 = cdfplot(y_u);
    c3 = cdfplot(y_h);
    
    %[p1,x1] = hist(y_c,50); plot(x1,p1/sum(p1));
    %[p2,x2] = hist(y_u,50); plot(x2,p2/sum(p2));
    %[p3,x3] = hist(y_h,50); plot(x3,p3/sum(p3));
    
    nbins = 50
    dist = 'Normal'
    %histogram(y_c, nbins, 'Normalization', 'pdf')
    %histogram(y_u, nbins, 'Normalization', 'pdf')
    %histogram(y_h, nbins, 'Normalization', 'pdf')
    
    %histfit(y_c, nbins, dist);
    %histfit(y_u, nbins, dist);
    %histfit(y_h, nbins, dist);
    
    %fitdist(y_c, 'Normal');
    %fitdist(y_u, 'Normal');
    %fitdist(y_h, 'Normal');
    
    legend('Cellular', 'Wi-Fi University', 'Wi-Fi Home', 'FontSize', font_size_legend, 'Location', legend_pos);
    %legend(sprintf('AT&T'), sprintf('FRGP'), sprintf('Qwest'), 'FontSize', font_size, 'Location', legend_pos);
    %columnlegend(3, 'Cellular', 'University Wifi', 'Home Wifi');
    hold off;
    title('');
    if base_station_core == 1
        xlabel('Base Station Latency (ms)')
    else
        xlabel('Core Network Latency (ms)')
    end
    
    set(c, 'LineStyle', '-', 'Color', '#4B288F');
    set(c2,'LineWidth', line_width);
    set(c2, 'LineStyle', '-', 'Color', '#F54FA1');
    set(c3,'LineWidth', line_width);
    set(c3, 'LineStyle', '-', 'Color', '#4AF896');
elseif plotnum == 5
    bar([4.5, 5, 5])
end
ylabel('CDF')
grid on;
axis square;

set(gca, 'YMinorTick','on', 'YMinorGrid','on')
set(gca, 'XMinorTick','on', 'XMinorGrid','on')
set(gca,'FontSize',font_size);


set(c,'LineWidth', line_width);
if plotnum ~= 4
    set(c, 'LineStyle', '-', 'Color', 'black');

    avg = mean(y);
    x_vals = get(c,'Xdata');
    y_vals = get(c,'Ydata');
    [d,ix] = min(abs(x_vals-avg));
    color = get(c, 'Color');
    xline(avg, 'LineWidth', line_width, 'LineStyle', '--', 'color', color, 'HandleVisibility','off');
else
    avg_c = mean(y_c);
    avg_u = mean(y_u);
    avg_h = mean(y_h);
    
    x_vals = get(c,'Xdata');
    y_vals = get(c,'Ydata');
    [d,ix] = min(abs(x_vals-avg_c));
    color = get(c, 'Color');
    xline(avg_c, 'LineWidth', line_width_dotted, 'LineStyle', '--', 'color', color, 'HandleVisibility','off');
    
    x_vals = get(c2,'Xdata');
    y_vals = get(c2,'Ydata');
    [d,ix] = min(abs(x_vals-avg_u));
    color = get(c2, 'Color');
    xline(avg_u, 'LineWidth', line_width_dotted, 'LineStyle', '--', 'color', color, 'HandleVisibility','off');
    
    x_vals = get(c3,'Xdata');
    y_vals = get(c3,'Ydata');
    [d,ix] = min(abs(x_vals-avg_h));
    color = get(c3, 'Color');
    xline(avg_h, 'LineWidth', line_width_dotted, 'LineStyle', '--', 'color', color, 'HandleVisibility','off');
    
    set(gca, 'XScale', 'log', 'XGrid', 'on', 'XMinorGrid', 'off');
%    set(gca, 'YScale', 'log', 'YGrid', 'on', 'YMinorGrid', 'on');
    xticks([5, 10, 20, 40, 80, 160, 320, 640, 1280]);
    set(gca,'XTickLabel',num2str(get(gca,'XTick').'));
    xlim([3.6, max([max(y_c), max(y_u), max(y_h) + 1000])])
end
