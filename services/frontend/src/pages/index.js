import Head from 'next/head';
import Chat from '../components/Chat';

export default function Home() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Head>
        <title>Legal Assistant Chatbot</title>
        <meta name="description" content="AI Legal Assistant for Romanian Law" />
      </Head>

      <main style={{ 
        flex: 1, 
        display: 'flex', 
        flexDirection: 'column',
        padding: '20px',
        maxWidth: '800px',
        margin: '0 auto',
        width: '100%'
      }}>
        <h1 style={{ textAlign: 'center', margin: '0 0 20px 0' }}>
          Romanian Legal Assistant
        </h1>
        <Chat />
      </main>
    </div>
  );
}
