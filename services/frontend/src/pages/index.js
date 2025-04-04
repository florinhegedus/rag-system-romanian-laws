import Head from 'next/head';
import Chat from '../components/Chat';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Legal Assistant Chatbot</title>
        <meta name="description" content="AI Legal Assistant for Romanian Law" />
      </Head>

      <main>
        <h1 style={{ textAlign: 'center', margin: '20px 0' }}>
          Romanian Legal Assistant
        </h1>
        <Chat />
      </main>
    </div>
  );
}
