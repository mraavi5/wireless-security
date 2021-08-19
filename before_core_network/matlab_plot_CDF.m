global show_windows marker_size line_width font_size;
show_windows = 'on';
marker_size = 15;
line_width = 2;
font_size = 18;

plotnum = 2

data = readmatrix('postprocessed_before_core_network_att-5g-100samples.csv', 'Delimiter', ',', 'LineEnding', '\n');

fig = figure();


if plotnum == 1
    y = data(:, 3)
    c = cdfplot(y);
    title('');
    xlabel('Base station latency (ms)')
else
    y = data(:, 4)
    c = cdfplot(y);
    title('');
    xlabel('Hops to base station')
end
grid on;
axis square;

set(gca, 'YMinorTick','on', 'YMinorGrid','on')
set(gca, 'XMinorTick','on', 'XMinorGrid','on')
set(gca,'FontSize',font_size);
set(c,'LineWidth', line_width);
set(c, 'LineStyle', '-', 'Color', 'black');


avg = mean(y);
x_vals = get(c,'Xdata');
y_vals = get(c,'Ydata');
[d,ix] = min(abs(x_vals-avg));
color = get(c, 'Color');
xline(avg, 'LineWidth', line_width, 'LineStyle', '--', 'color', color, 'HandleVisibility','off');

%xticks([0, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000]);
%set(gca,'XTickLabel',num2str(get(gca,'XTick').'));