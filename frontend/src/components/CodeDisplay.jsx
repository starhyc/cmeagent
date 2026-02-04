import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';

export default function CodeDisplay({ code, language }) {
  return (
    <SyntaxHighlighter language={language}>
      {code}
    </SyntaxHighlighter>
  );
}
