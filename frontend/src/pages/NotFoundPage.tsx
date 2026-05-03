import { Link, useNavigate } from 'react-router-dom';
import { Home, ArrowLeft } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-[60vh] items-center justify-center px-4">
      <Card className="w-full max-w-md text-center">
        <CardHeader>
          <CardTitle className="text-6xl font-black text-ketchup">404</CardTitle>
          <CardDescription className="text-lg">Page non trouvée</CardDescription>
        </CardHeader>

        <CardContent className="flex flex-col items-center gap-6">
          <p className="text-muted-foreground">
            Oups ! La page que vous recherchez n'existe pas ou a été déplacée.
          </p>

          <div className="flex w-full flex-col justify-space-between gap-4 sm:flex-row sm:justify-center">
            <Button onClick={() => navigate(-1)} variant="outline">
              <ArrowLeft />
              Retour
            </Button>
            <Button asChild>
              <Link to="/">
                <Home />
                Accueil
              </Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
