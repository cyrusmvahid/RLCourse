import QtQuick 2.0

Rectangle {
 width: 200
 height: 200
 color: "green"

Text {
 text: "Hello World"
 anchors.centerIn: parent
 }
}





function drawBoard(num_rows, num_cols){
    context = myGameArea.context;

    bw = context.canvas.width;
    cell_width = Math.floor(bw / num_rows);

    bh = context.canvas.height;
    cell_height = Math.floor(bh / num_cols);
    // Padding
    p = 0;

    for (var x = 0; x <= bw; x += cell_width) {
        context.moveTo(0.5 + x + p, p);
        context.lineTo(0.5 + x + p, bh + p);
    }


    for (x = 0; x <= bh; x += cell_height) {
        context.moveTo(p, 0.5 + x + p);
        context.lineTo(bw + p, 0.5 + x + p);
    }

    context.strokeStyle = "black";
    context.stroke();
}
