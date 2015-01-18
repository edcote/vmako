 <%include file="v.mako"/>

 module dff_ares_${w} (
  input clk,
  input ares,
  input [${e(w-1)}:0] d,
  output reg [${e(w-1)}:0] q
);

  always @(posedge clk or posedge ares)
    if (ares)
      q <= 0;
    else
      q <= d;

endmodule