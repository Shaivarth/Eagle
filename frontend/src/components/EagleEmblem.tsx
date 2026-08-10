import "./EagleEmblem.css";

export default function EagleEmblem() {
  const asciiEagle = [
    "                        z$b",
    "               .e$$$b.  $$$F  .d$$be",
    "           .d$$$$$$$$$$e$$$be$$$$$$$$$$e.",
    "       .e$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$b.",
    "     z$$$$$$$P**\"\"**$$$$$$$$$$$P*\"\"\"\"***$$$$$b.",
    "   z$$$$*\"            \"$$$$$$\"            \"*$$$$c",
    " z$$*\"                 ^$$$$                  \"*$$.",
    "^\"                      $$$F                      ^%",
    "                        $$$b",
    "                        $P*$",
    "                       4P  *r",
    "                       4    %",
  ].join("\n");

  return (
    <div className="eagle-jet-container">
      <pre className="eagle-jet-ascii">{asciiEagle}</pre>
    </div>
  );
}
